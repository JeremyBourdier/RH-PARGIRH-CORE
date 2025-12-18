import streamlit as st
import pandas as pd
import numpy as np

class EconomicModule:
    def __init__(self):
        # Configuración por defecto de cultivos
        self.cultivos_default = {
            'Arroz': {'s': 4500, 'i': 2000},
            'Banano': {'s': 2500, 'i': 3500},
            'Aguacate': {'s': 1800, 'i': 5000}
        }

    def get_dummy_data(self):
        # Genera datos simulados solo para este módulo
        dates = pd.date_range(start='2020-01-01', periods=60, freq='ME')
        np.random.seed(42)
        pr = np.random.gamma(shape=2, scale=30, size=len(dates))
        pr[-10:] = pr[-10:] * 0.1 # Simular sequía al final
        tmax = np.random.normal(30, 2, size=len(dates))
        return pd.DataFrame({'Fecha': dates, 'pr': pr, 'TMAX': tmax})

    def calcular_perdidas(self, df, costos):
        df_sim = df.copy()
        
        # 1. Lógica Hidrológica Simplificada
        df_sim['Recarga_pr'] = df_sim['pr'].rolling(3).mean().shift(1).fillna(0)
        df_sim['Agotamiento'] = df_sim['TMAX'] * 1.5
        df_sim['Caudal_Logico'] = df_sim['Recarga_pr'] - df_sim['Agotamiento']
        
        # 2. Umbrales Dinámicos
        p10 = df_sim['Caudal_Logico'].quantile(0.10)
        p90 = df_sim['Caudal_Logico'].quantile(0.90)
        
        # 3. Severidad
        df_sim['Severidad_Sequia'] = np.where(df_sim['Caudal_Logico'] < p10, abs(df_sim['Caudal_Logico'] - p10), 0)
        df_sim['Severidad_Inundacion'] = np.where(df_sim['Caudal_Logico'] > p90, abs(df_sim['Caudal_Logico'] - p90), 0)
        
        # 4. Cálculo Económico
        for cult, params in costos.items():
            perdida = (df_sim['Severidad_Sequia'] * params['Sequia']) + \
                      (df_sim['Severidad_Inundacion'] * params['Inundacion'])
            df_sim[f'Perdida_{cult}'] = perdida
            
        return df_sim, p10, p90

    def render(self):
        st.subheader("🌾 Estimación de Impacto Agrícola (Modelo FAO 33)")
        st.markdown("---")
        
        # --- A. CONTROLES (Dentro de la pestaña, para no ensuciar el Sidebar principal) ---
        col_controls, col_graphs = st.columns([1, 3])
        
        costos_config = {}
        with col_controls:
            st.info("⚙️ **Calibración de Costos (DOP)**")
            for cult, vals in self.cultivos_default.items():
                with st.expander(f"Precios: {cult}", expanded=False):
                    s = st.slider(f"Sequía", 0, 10000, vals['s'], key=f"s_{cult}_eco")
                    i = st.slider(f"Inundación", 0, 10000, vals['i'], key=f"i_{cult}_eco")
                    costos_config[cult] = {'Sequia': s, 'Inundacion': i}
        
        # --- B. CÁLCULOS ---
        df = self.get_dummy_data() # Usamos data simulada segura
        df_final, p10, p90 = self.calcular_perdidas(df, costos_config)
        
        # --- C. VISUALIZACIÓN ---
        with col_graphs:
            # KPI Principal
            cols_perdida = [c for c in df_final.columns if 'Perdida_' in c]
            total_perdida = df_final[cols_perdida].sum().sum()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Pérdida Total Estimada", f"RD$ {total_perdida:,.0f}")
            c2.metric("Umbral Sequía (P10)", f"{p10:.1f}")
            c3.metric("Umbral Inundación (P90)", f"{p90:.1f}")
            
            # Gráficas
            tab_g1, tab_g2 = st.tabs(["📉 Dinero Perdido", "💧 Caudal Lógico"])
            
            with tab_g1:
                st.bar_chart(df_final.set_index('Fecha')[cols_perdida])
                
            with tab_g2:
                st.line_chart(df_final.set_index('Fecha')['Caudal_Logico'])
                
            with st.expander("Ver Datos Detallados"):
                st.dataframe(df_final.tail(10))
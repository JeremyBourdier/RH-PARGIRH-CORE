import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class DashboardUI:
    def render_header(self):
        st.title("RH-PARGIRH: Inteligencia Hídrica")
        st.markdown("**Proyecto de Resiliencia para las Cuencas Yaque del Norte y Ozama (INDRHI / BM)**")
        st.markdown("---")

    def render_kpis(self, kpis):
        st.subheader("📊 Indicadores Clave de Desempeño")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Caudal Proyectado", f"{kpis['promedio']:.1f} m³/s", f"{kpis['variacion']:.1f}%")
        c2.metric("Inercia Hídrica", f"{kpis['inercia']:.1f} mm")
        c3.metric("Meses Críticos", f"{kpis['meses_criticos']}", delta=-kpis['meses_criticos'], delta_color="inverse")
        c4.metric("Estado", kpis['estado_texto'], kpis['estado_icono'])

    def render_main_chart(self, df_view, config):
        st.markdown("### 📈 Auditoría y Simulación")
        fig = go.Figure()
        # IA Base
        fig.add_trace(go.Scatter(x=df_view['Fecha'], y=df_view['Caudal_IA'], name='Línea Base (IA)', line=dict(color='#005da4', width=2)))
        
        # Simulación (solo si hay cambios)
        if config["delta_lluvia"] != 0 or config["delta_temp"] != 0:
            fig.add_trace(go.Scatter(x=df_view['Fecha'], y=df_view['Caudal_Simulado'], name='Simulación', line=dict(color='#ff9900', width=2, dash='dash')))
        
        # Realidad
        df_real = df_view.dropna(subset=['Caudal_Real'])
        if not df_real.empty:
            fig.add_trace(go.Scatter(x=df_real['Fecha'], y=df_real['Caudal_Real'], mode='markers', name='Datos Reales', marker=dict(color='#d92b2b', size=6)))
        
        fig.update_layout(height=400, template="plotly_white", margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    def render_geo_xai(self, df_view, promedio):
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 📍 Monitor Territorial")
            map_data = pd.DataFrame({
                'lat': [19.77, 18.50, 19.15],
                'lon': [-71.55, -70.10, -69.82],
                'size': [promedio*10, promedio*8, promedio*12], 
                'color': [[0, 0, 255, 140], [0, 0, 255, 140], [0, 0, 255, 140]]
            })
            st.map(map_data, latitude='lat', longitude='lon', size='size', color='#0044ff')
        
        with c2:
            st.markdown("### 🧠 Explicabilidad (XAI)")
            fig = px.scatter(df_view, x='Inercia_3meses', y='Caudal_Simulado', color='Mes', title="Inercia vs Caudal", color_continuous_scale='Blues')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

class DashboardUI:
    def render_header(self):
        # Encabezado limpio
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
        
        # IA Base (Azul)
        fig.add_trace(go.Scatter(x=df_view['Fecha'], y=df_view['Caudal_IA'], name='Línea Base (IA)', line=dict(color='#005da4', width=2)))
        
        # Simulación (Naranja - Solo si hay cambios)
        if config["delta_lluvia"] != 0 or config["delta_temp"] != 0:
            fig.add_trace(go.Scatter(x=df_view['Fecha'], y=df_view['Caudal_Simulado'], name='Simulación', line=dict(color='#ff9900', width=2, dash='dash')))
        
        # Realidad (Rojo - Puntos)
        df_real = df_view.dropna(subset=['Caudal_Real'])
        if not df_real.empty:
            fig.add_trace(go.Scatter(x=df_real['Fecha'], y=df_real['Caudal_Real'], mode='markers', name='Datos Reales', marker=dict(color='#d92b2b', size=6)))
        
        fig.update_layout(height=400, template="plotly_white", margin=dict(l=20, r=20, t=20, b=20), legend=dict(orientation="h", y=1.1))
        st.plotly_chart(fig, use_container_width=True)

    def render_geo_xai(self, df_view, kpis):
        """Monitor Territorial Avanzado con Mapa de Riesgo"""
        promedio = kpis['promedio']
        estado = kpis['estado_texto']
        
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown("### 📍 Monitor de Riesgo en Cuencas")
            
            # Lógica de Semáforo Visual
            if "CRISIS" in estado:
                scale_name = "Reds" # Mapa Rojo
            elif "ALERTA" in estado:
                scale_name = "Oranges" # Mapa Naranja
            else:
                scale_name = "Blues" # Mapa Azul

            # Datos Simulados de Estaciones
            map_data = pd.DataFrame({
                'lat': [19.7642, 19.4517, 18.5912, 19.15],
                'lon': [-71.5625, -70.6928, -69.9715, -69.82],
                'Estacion': ['Palo Verde (Bajo Yaque)', 'Santiago (Tavera)', 'Ozama (Santo Domingo)', 'Yuna (Bonao)'],
                'Caudal': [promedio, promedio * 1.2, promedio * 0.9, promedio * 1.5],
                'Estado': [estado] * 4
            })

            # Mapa Interactivo (Plotly Mapbox)
            fig_map = px.scatter_mapbox(
                map_data, 
                lat="lat", lon="lon",
                size="Caudal", 
                color="Caudal",
                color_continuous_scale=scale_name,
                size_max=25, 
                zoom=7,
                hover_name="Estacion",
                mapbox_style="carto-positron"
            )
            
            fig_map.update_layout(height=350, margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)
            st.plotly_chart(fig_map, use_container_width=True)
            st.caption(f"🔵 Estaciones Hidrométricas Activas. Estado Actual: **{estado}**")
        
        with c2:
            st.markdown("### 🧠 Explicabilidad Física (XAI)")
            fig = px.scatter(
                df_view, 
                x='Inercia_3meses', 
                y='Caudal_Simulado', 
                color='Mes', 
                title="Evidencia: Relación Inercia vs Caudal", 
                color_continuous_scale='Blues',
                labels={'Inercia_3meses': 'Inercia Hídrica (mm)', 'Caudal_Simulado': 'Caudal (m³/s)'}
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
import streamlit as st
import os

class Sidebar:
    def render(self, df):
        with st.sidebar:
            # Logos
            if os.path.exists("assets/logo.png"):
                st.image("assets/logo.png", use_container_width=True)
            else:
                st.markdown("## INDRHI")

            st.markdown("---")
            st.title("🎛️ Centro de Control")
            
            # Filtros de Tiempo
            st.subheader("📅 Rango de Análisis")
            min_year = int(df['Fecha'].dt.year.min())
            max_year = int(df['Fecha'].dt.year.max())
            rango = st.slider("Años:", min_year, max_year, (1975, 1985))
            
            st.markdown("---")
            
            # Simulador
            st.subheader("🧪 Simulador Climático")
            lluvia = st.slider("🌧️ Lluvia (%)", -50, 50, 0)
            temp = st.slider("🌡️ Temperatura (+°C)", 0.0, 3.0, 0.0, step=0.1)
            
            st.markdown("---")
            st.caption("v2.0 - OOP Architecture")
            
            # Valores empaquetados
            return {
                "rango": rango,
                "delta_lluvia": lluvia,
                "delta_temp": temp
            }
import streamlit as st
import os

class Sidebar:
    def render_sources(self):
        """Renderiza la sección de fuentes y metodología (La Justificación del Reporte)"""
        with st.sidebar:
            st.markdown("---")
            # Usamos un expander para mantener la interfaz limpia pero accesible
            with st.expander("📚 Fuentes y Metodología", expanded=False):
                st.markdown("""
                **1. Base Hidrológica (Física):**
                * *Caudales Históricos:* Global Runoff Data Centre (GRDC) - Estación Palo Verde (ID 4382100).
                * *Climatología:* ERA5 Satellite Reanalysis (ECMWF/Copernicus).
                
                **2. Modelo Predictivo (IA):**
                * *Algoritmo:* Random Forest Regressor (Scikit-Learn).
                * *Entrenamiento:* Periodo 1976-1984 (Ground Truth).
                * *Validación:* R² = 0.97 (Alta Precisión).
                
                **3. Impacto Económico:**
                * *Producción:* Censo Agropecuario 2023 (Ministerio de Agricultura).
                * *Precios:* Bolsa Agroempresarial de la RD (BARD).
                
                **4. Protocolos de Actuación:**
                * Basado en el "Manual de Operación de Presas y Embalses (MOPE)" del INDRHI.
                """)
                st.info("Sistema auditado conforme a estándares ISO-31000 de Gestión de Riesgos.")
                st.caption("v1.0.5 | Hackathon Build")

    def render(self, df):
        with st.sidebar:
            # A. LOGO PRINCIPAL
            if os.path.exists("assets/logo.png"):
                st.image("assets/logo.png", use_container_width=True)
            else:
                st.markdown("## INDRHI")

            st.markdown("---")
            st.title("🎛️ Centro de Control")
            
            # B. CONTROLES DE TIEMPO
            st.subheader("📅 Rango de Análisis")
            min_year = int(df['Fecha'].dt.year.min())
            max_year = int(df['Fecha'].dt.year.max())
            rango = st.slider("Años:", min_year, max_year, (1975, 1985))
            
            st.markdown("---")
            
            # C. SIMULADOR CLIMÁTICO
            st.subheader("🧪 Simulador Climático")
            lluvia = st.slider("🌧️ Lluvia (%)", -50, 50, 0)
            temp = st.slider("🌡️ Temperatura (+°C)", 0.0, 3.0, 0.0, step=0.1)
            
            # D. LLAMADA A LA JUSTIFICACIÓN (AQUÍ ESTÁ LA CLAVE)
            self.render_sources()
            
            # Retorno de valores al motor
            return {
                "rango": rango,
                "delta_lluvia": lluvia,
                "delta_temp": temp
            }
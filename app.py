import streamlit as st
# Importamos nuestras clases (Módulos)
from modules.data_loader import DataLoader
from modules.sidebar import Sidebar
from modules.engine import HydrologyEngine
from modules.dashboard import DashboardUI
from modules.reporter import ReportGenerator

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="RH-PARGIRH Core", page_icon="💧", layout="wide", initial_sidebar_state="expanded")

# Inyectar CSS global (puedes dejar esto aquí o moverlo a otro lado)
st.markdown("""<style>[data-testid="stAppViewContainer"] {background-color: #f8f9fa; color: #31333F;} h1,h2,h3 {color: #003366 !important; font-family: 'Segoe UI';}</style>""", unsafe_allow_html=True)

# --- 2. ORQUESTACIÓN DE LA APP ---
def main():
    # A. Cargar Datos
    loader = DataLoader()
    df = loader.load_data()
    
    if df is None:
        st.error("🚨 No se encuentran los datos.")
        st.stop()

    # B. Renderizar Sidebar y Obtener Configuración
    sidebar = Sidebar()
    config = sidebar.render(df)

    # C. Ejecutar Motor Lógico (Simulación)
    engine = HydrologyEngine(df)
    df_simulated = engine.run_simulation(config)
    kpis = engine.calculate_kpis(df_simulated)

    # D. Renderizar Dashboard Principal
    dashboard = DashboardUI()
    dashboard.render_header()
    dashboard.render_kpis(kpis)
    dashboard.render_main_chart(df_simulated, config)
    dashboard.render_geo_xai(df_simulated, kpis['promedio'])

    # E. Renderizar Reportes
    reporter = ReportGenerator()
    reporter.render_button(df_simulated, kpis)

if __name__ == "__main__":
    main()
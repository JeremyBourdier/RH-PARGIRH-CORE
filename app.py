import streamlit as st
# Módulos
from modules.data_loader import DataLoader
from modules.sidebar import Sidebar
from modules.engine import HydrologyEngine
from modules.dashboard import DashboardUI
from modules.reporter import ReportGenerator
from modules.chatbot import LegalAssistant

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="RH-PARGIRH Core", page_icon="💧", layout="wide", initial_sidebar_state="expanded")

# Inyectar CSS global 
st.markdown("""
<style>
    /* 1. Ajuste del Contenedor Principal */
    .block-container {
        padding-top: 3rem !important; /* Espacio seguro para no cortar el título */
        padding-bottom: 1rem !important;
    }
    
    /* 2. Tema Claro Forzado */
    [data-testid="stAppViewContainer"] {
        background-color: #f8f9fa; 
        color: #31333F;
    }
    
    /* 3. Títulos Institucionales */
    h1, h2, h3 {
        color: #003366 !important; 
        font-family: 'Segoe UI', sans-serif;
    }

    /* 4. TARJETAS DE MÉTRICAS (KPIs) - ESTILO FINAL */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-left: 6px solid #005da4;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }

    /* EFECTO HOVER (FLOTAR) */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        border-color: #005da4;
    }

    /* ARREGLAR TAMAÑO DE NÚMEROS */
    [data-testid="stMetricValue"] {
        color: #333;
        font-weight: 700;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #666;
    }
</style>
""", unsafe_allow_html=True)

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
    if config["delta_lluvia"] != 0 or config["delta_temp"] != 0:
        st.toast(f"🔄 Recalculando modelo: Lluvia {config['delta_lluvia']}% | Temp +{config['delta_temp']}°C", icon="🧮")
    df_simulated = engine.run_simulation(config)
    kpis = engine.calculate_kpis(df_simulated)

    # D. Renderizar Dashboard Principal
    dashboard = DashboardUI()
    dashboard.render_header()
    dashboard.render_kpis(kpis)
    dashboard.render_main_chart(df_simulated, config)
    dashboard.render_geo_xai(df_simulated, kpis)

    # E. Renderizar Reportes
    reporter = ReportGenerator()
    reporter.render_button(df_simulated, kpis)
    
    with st.sidebar:
      bot = LegalAssistant()
      bot.render()

if __name__ == "__main__":
    main()
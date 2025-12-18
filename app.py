import streamlit as st
# Módulos
from modules.data_loader import DataLoader
from modules.sidebar import Sidebar
from modules.engine import HydrologyEngine
from modules.dashboard import DashboardUI
from modules.reporter import ReportGenerator
from modules.chatbot import LegalAssistant
from modules.economics import EconomicModule
from modules.governance import GovernanceModule

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="RH-PARGIRH Core", page_icon="💧", layout="wide", initial_sidebar_state="expanded")

# Inyectar CSS global 
# Cuando tengo el tema de oscuridad me da problemas, tengo que tener el navegador en modo claro para que los colores se vean bien.
st.markdown("""
<style>
    .block-container { padding-top: 2rem !important; padding-bottom: 1rem !important; }
    [data-testid="stAppViewContainer"] { background-color: #f8f9fa; color: #31333F; }
    h1, h2, h3 { color: #003366 !important; font-family: 'Segoe UI', sans-serif; }
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-left: 6px solid #005da4;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    div[data-testid="metric-container"]:hover { transform: translateY(-5px); box-shadow: 0 8px 15px rgba(0,0,0,0.15); border-color: #005da4; }
    [data-testid="stMetricValue"] { color: #333; font-weight: 700; }
    [data-testid="stMetricLabel"] { font-size: 0.9rem; color: #666; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #ffffff; border-radius: 5px 5px 0px 0px; gap: 1px; }
    .stTabs [aria-selected="true"] { background-color: #e6f3ff; border-bottom: 2px solid #005da4; color: #005da4; }
</style>
""", unsafe_allow_html=True)

# --- 2. ORQUESTACIÓN DE LA APP ---
def main():
    # A. Cargar Datos
    loader = DataLoader()
    df = loader.load_data()
    
    if df is None:
        st.error("🚨 No se encuentran los datos. Revisa la conexión.")
        st.stop()

    # B. Renderizar Sidebar y Obtener Configuración
    sidebar = Sidebar()
    config = sidebar.render(df)

    # C. Ejecutar Motor Lógico (Simulación Hídrica)
    engine = HydrologyEngine(df)
    
    if config["delta_lluvia"] != 0 or config["delta_temp"] != 0:
        st.toast(f"🔄 Recalculando modelo: Lluvia {config['delta_lluvia']}% | Temp +{config['delta_temp']}°C", icon="🧮")
        
    df_simulated = engine.run_simulation(config)
    kpis = engine.calculate_kpis(df_simulated)

    # --- D. INTERFAZ PRINCIPAL CON PESTAÑAS ---
    st.title("RH-PARGIRH: Sistema de Gestión Integrada")
    
   # Pestañas
    tab_hidrica, tab_economica, tab_gobernabilidad = st.tabs(["💧 Inteligencia Hídrica", "💰 Impacto Económico", "⚖️ Gobernabilidad"])

    # Pestaña 1
    with tab_hidrica:
        dashboard = DashboardUI()
        # dashboard.render_header() # Opcional
        dashboard.render_kpis(kpis)
        dashboard.render_main_chart(df_simulated, config)
        dashboard.render_geo_xai(df_simulated, kpis)

        st.markdown("---")
        reporter = ReportGenerator()
        reporter.render_button(df_simulated, kpis)

    # Pestaña 2
    with tab_economica:
        economy = EconomicModule()
        economy.render()
        
    # Pestaña 3
    with tab_gobernabilidad:
        gov = GovernanceModule()
        gov.render(kpis)

    # E. Chatbot en Sidebar 
    with st.sidebar:
        bot = LegalAssistant()
        bot.render()

if __name__ == "__main__":
    main()
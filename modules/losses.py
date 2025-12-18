import streamlit as st
import pandas as pd
import numpy as np

# --- 1. GENERACIÓN DE DATOS SIMULADOS (Para que funcione sin CSVs jijijij) ---
def get_dummy_data():
    dates = pd.date_range(start='2020-01-01', periods=60, freq='ME')
    np.random.seed(42)
    # Simulamos un ciclo de lluvia con sequía al final
    pr = np.random.gamma(shape=2, scale=30, size=len(dates)) 
    pr[-10:] = pr[-10:] * 0.1 # Simular sequía severa al final
    tmax = np.random.normal(30, 2, size=len(dates))
    
    df = pd.DataFrame({'Fecha': dates, 'pr': pr, 'TMAX': tmax})
    return df

# --- 2. LÓGICA CORE (Caudal Lógico) ---
def generar_alertas(df):
    df_out = df.copy()
    # Recarga (Inercia 3 meses)
    df_out['Recarga_pr'] = df_out['pr'].rolling(3).mean().shift(1).fillna(0)
    df_out['Agotamiento'] = df_out['TMAX'] * 1.5
    df_out['Caudal_Logico'] = df_out['Recarga_pr'] - df_out['Agotamiento']
    return df_out

# --- 3. MOTOR PARAMÉTRICO DE PÉRDIDAS (FAO 33 SIMPLIFICADO) ---
def motor_estimacion(df, p10, p90, costos):
    df_sim = df.copy()
    
    # Cálculo de Severidad (Física)
    df_sim['Severidad_Sequia'] = np.where(df_sim['Caudal_Logico'] < p10, abs(df_sim['Caudal_Logico'] - p10), 0)
    df_sim['Severidad_Inundacion'] = np.where(df_sim['Caudal_Logico'] > p90, abs(df_sim['Caudal_Logico'] - p90), 0)
    
    # Cálculo Económico (Dinámico)
    for cultivo, params in costos.items():
        perdida = (df_sim['Severidad_Sequia'] * params['Sequia']) + \
                  (df_sim['Severidad_Inundacion'] * params['Inundacion'])
        df_sim[f'Perdida_{cultivo}'] = perdida
        
    return df_sim

# --- 4. INTERFAZ STREAMLIT ---
st.set_page_config(page_title="RH-PARGIRH | Módulo Económico", layout="wide")

st.title("🌾 RH-PARGIRH: Estimación de Impacto Agrícola")
st.markdown("**Metodología:** Umbrales Hidrológicos (P10/P90) + Costos de Producción (Paramétricos).")

# --- SIDEBAR: CALIBRACIÓN ---
st.sidebar.header("⚙️ Calibración Agronómica")
st.sidebar.info("Ajuste los costos por unidad de severidad hídrica.")

costos_config = {}
cultivos = ['Arroz', 'Banano', 'Aguacate']

for cult in cultivos:
    st.sidebar.subheader(f"Costos para {cult} (DOP)")
    s = st.sidebar.slider(f"{cult} - Impacto Sequía", 0, 10000, 4500 if cult=='Arroz' else 2000)
    i = st.sidebar.slider(f"{cult} - Impacto Inundación", 0, 10000, 2000 if cult=='Arroz' else 5000)
    costos_config[cult] = {'Sequia': s, 'Inundacion': i}

# --- EJECUCIÓN ---
df_clima = get_dummy_data()
df_processed = generar_alertas(df_clima)

# Calculamos P10/P90 dinámicamente sobre la serie
p10 = df_processed['Caudal_Logico'].quantile(0.10)
p90 = df_processed['Caudal_Logico'].quantile(0.90)

df_final = motor_estimacion(df_processed, p10, p90, costos_config)

# --- VISUALIZACIÓN ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1. Monitor de Caudal Lógico")
    chart_data = df_final.set_index('Fecha')[['Caudal_Logico']]
    st.line_chart(chart_data)
    # Dibujar umbrales manualmente es difícil en st.line_chart simple, 
    # pero explicamos que las líneas invisibles son P10={p10:.1f} y P90={p90:.1f}
    st.caption(f"Umbrales Detectados: Sequía (P10) = {p10:.2f} | Inundación (P90) = {p90:.2f}")

with col2:
    st.subheader("2. Pérdidas Estimadas (DOP)")
    cols_perdida = [c for c in df_final.columns if 'Perdida_' in c]
    total_perdida = df_final[cols_perdida].sum().sum()
    st.metric("Pérdida Total Acumulada", f"RD$ {total_perdida:,.0f}")
    
    st.bar_chart(df_final.set_index('Fecha')[cols_perdida].sum(axis=1))

st.subheader("Detalle de Datos (Últimos 5 meses)")
st.dataframe(df_final.tail(5))
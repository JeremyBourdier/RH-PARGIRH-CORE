import pytest
import pandas as pd
from modules.engine import HydrologyEngine

# 1. Mock Data
@pytest.fixture
def dummy_data():
    data = {
        'Fecha': pd.to_datetime(['2020-01-01', '2020-02-01', '2020-03-01']),
        'Caudal_IA': [30.0, 40.0, 35.0], # Caudal base
        'Inercia_3meses': [50.0, 60.0, 55.0],
        'Mes': [1, 2, 3],
        'Caudal_Real': [31.0, 41.0, 34.0]
    }
    return pd.DataFrame(data)

# 2. Test: ¿El simulador reduce el caudal si hay sequía?
def test_simulacion_sequia(dummy_data):
    engine = HydrologyEngine(dummy_data)
    
    # Configuración: -50% Lluvia, +0°C Temp
    config = {
        "rango": (2020, 2020),
        "delta_lluvia": -50,
        "delta_temp": 0.0
    }
    
    # Ejecutar simulación
    df_sim = engine.run_simulation(config)
    
    # Verificación
    # Si la lluvia baja 50%, el caudal simulado debe ser la mitad del base
    caudal_base = df_sim['Caudal_IA'].iloc[0]
    caudal_sim = df_sim['Caudal_Simulado'].iloc[0]
    
    # Assert 
    assert caudal_sim == caudal_base * 0.5
    print(f"Test Sequía: Base {caudal_base} -> Sim {caudal_sim}. ¡Correcto!")

# 3. Test: ¿Detecta Crisis Hídrica?
def test_detecta_crisis(dummy_data):
    # Forzamos datos muy bajos para que salte la crisis
    dummy_data['Caudal_IA'] = [10.0, 10.0, 10.0] 
    engine = HydrologyEngine(dummy_data)
    
    config = {"rango": (2020, 2020), "delta_lluvia": 0, "delta_temp": 0}
    df_sim = engine.run_simulation(config)
    kpis = engine.calculate_kpis(df_sim)
    
    # Assert
    assert "CRISIS" in kpis['estado_texto']
    print("Test Crisis: El sistema detectó correctamente la alerta roja.")
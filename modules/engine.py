import pandas as pd

class HydrologyEngine:
    def __init__(self, df):
        self.df = df

    def run_simulation(self, config):
        """Ejecuta la simulación física basada en los inputs del usuario"""
        start_year, end_year = config["rango"]
        delta_lluvia = config["delta_lluvia"]
        delta_temp = config["delta_temp"]

        # 1. Filtrar
        df_view = self.df[(self.df['Fecha'].dt.year >= start_year) & (self.df['Fecha'].dt.year <= end_year)].copy()

        # 2. Calcular Factores Físicos
        factor_lluvia = 1 + (delta_lluvia / 100)
        factor_temp = 1 - (delta_temp * 0.05) # Hipótesis: +1°C = -5% caudal
        
        # 3. Generar Columna Simulada
        df_view['Caudal_Simulado'] = df_view['Caudal_IA'] * factor_lluvia * factor_temp
        
        return df_view

    def calculate_kpis(self, df_view):
        """Calcula métricas clave para el dashboard"""
        promedio_actual = df_view['Caudal_Simulado'].mean()
        promedio_base = df_view['Caudal_IA'].mean()
        variacion = ((promedio_actual - promedio_base) / promedio_base) * 100
        inercia = df_view['Inercia_3meses'].mean()
        meses_criticos = len(df_view[df_view['Caudal_Simulado'] < 20])
        
        # Lógica de Estado
        if promedio_actual < 20:
            estado = ("CRISIS HÍDRICA", "🔴", "inverse")
        elif promedio_actual < 35:
            estado = ("ALERTA PREVENTIVA", "🟡", "off")
        else:
            estado = ("NORMALIDAD", "🟢", "normal")
            
        return {
            "promedio": promedio_actual,
            "variacion": variacion,
            "inercia": inercia,
            "meses_criticos": meses_criticos,
            "estado_texto": estado[0],
            "estado_icono": estado[1],
            "color_kpi": estado[2]
        }
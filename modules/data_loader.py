import streamlit as st
import pandas as pd
import os

class DataLoader:
    def __init__(self):
        # Define las rutas posibles
        self.relative_path = os.path.join("data", "gold", "app_data_70years.csv")
        self.absolute_path = r"C:\Users\bourd\source\repos\RH-PARGIRH-CORE\data\gold\app_data_70years.csv"

    @st.cache_data
    def load_data(_self):
        """Carga y cachea los datos. El _self es un truco de Streamlit para el cache."""
        if os.path.exists(_self.relative_path):
            df = pd.read_csv(_self.relative_path)
        elif os.path.exists(_self.absolute_path):
            df = pd.read_csv(_self.absolute_path)
        else:
            return None
            
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df
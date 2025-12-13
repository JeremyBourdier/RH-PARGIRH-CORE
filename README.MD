# 💧 RH-PARGIRH Core: Inteligencia Hídrica
### Sistema de Soporte a la Decisión (DSS) para la Resiliencia Climática

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rh-pargirh-core-kubnrwukwqkwky5s9hfw9g.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Build Status](https://img.shields.io/badge/Build-Passing-brightgreen.svg)]()
[![AI Model](https://img.shields.io/badge/AI-RandomForest-orange)]()

> **Protegiendo la inversión de US$80 Millones del Proyecto PARGIRH (Banco Mundial / INDRHI) mediante Inteligencia Artificial.**

---

## 🎯 El Problema
Las cuencas del **Yaque del Norte** y **Ozama** son vitales para la seguridad hídrica y alimentaria de la República Dominicana. Sin embargo, la variabilidad climática extrema hace que los métodos tradicionales de gestión de embalses sean insuficientes, poniendo en riesgo la agricultura, el agua potable y la infraestructura.

## 💡 La Solución: RH-PARGIRH Core
Una plataforma de inteligencia estratégica que permite simular escenarios climáticos futuros, visualizar riesgos físicos/económicos y generar directrices operativas automáticas basadas en la ley.

### 🔗 [VER DEMO EN VIVO AHORA](https://rh-pargirh-core-kubnrwukwqkwky5s9hfw9g.streamlit.app/)

---

## 🚀 Funcionalidades Clave

### 1. 🧠 Motor de IA Predictiva
Utilizamos un modelo de **Random Forest Regressor** validado (R² = 0.97) que aprende de 70 años de historia hidrológica para predecir el caudal ante cambios de temperatura y lluvia.

### 2. 🎛️ Simulador de Escenarios ("What-If")
Permite a los tomadores de decisiones ajustar variables en tiempo real:
* *¿Qué pasa si llueve un 50% menos los próximos 3 meses?*
* *¿Cómo afecta un aumento de 2°C a la inercia del suelo?*

### 3. 📍 Monitor de Riesgo Territorial
Mapa interactivo que traduce los datos hidrológicos en un **Semáforo de Alerta** (🔴 Crisis / 🟡 Alerta / 🔵 Normal), mostrando visualmente el impacto en estaciones críticas (Palo Verde, Tavera, etc.).

### 4. 📄 Reportes Estratégicos Automatizados
Generación instantánea de **Memorándums Ejecutivos** listos para firmar.
* Incluye análisis de datos, impacto económico y **órdenes operativas legales** (basadas en el Manual de Operación de Presas).
* Persistencia de sesión y descarga en formato oficial.

### 5. 🤖 Asistente Legal (Chatbot IA)
Un agente inteligente integrado en la barra lateral que responde consultas sobre protocolos regulatorios citando artículos específicos del *Manual de Operación de Presas y Embalses (MOPE)*.

---

## 🛠️ Arquitectura Técnica

El proyecto sigue una arquitectura **Modular Orientada a Objetos** para garantizar escalabilidad y mantenimiento.

```mermaid
graph TD
    A[Data Loader] -->|Raw Data| B(Hydrology Engine)
    B -->|Simulation| C{Random Forest Model}
    C -->|Predictions| D[Dashboard UI]
    D -->|Visuals| E[Risk Map]
    D -->|Stats| F[Economic Impact]
    D -->|Alerts| G[Report Generator]

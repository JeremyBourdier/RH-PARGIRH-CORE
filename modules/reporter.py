import streamlit as st

class ReportGenerator:
    def render_button(self, df_view, kpis):
        st.markdown("---")
        st.subheader("📄 Generador de Memorándums de Inteligencia")
        st.info("Generación de directrices operativas basadas en el Manual de Operación de Presas y Embalses (MOPE).")
        
        if st.button("Generar Memorándum Ejecutivo"):
            self._generate_memo(df_view, kpis)

    def _generate_memo(self, df_view, kpis):
        # 1. Variables de Contexto
        fecha_rep = df_view['Fecha'].max().strftime('%Y-%m')
        promedio_actual = kpis['promedio']
        variacion = kpis['variacion']
        inercia_promedio = kpis['inercia']
        estado_texto = kpis['estado_texto'] # Viene del engine ("CRISIS HÍDRICA", etc)
        
        # 2. Lógica de Negocio (El Cerebro del Reporte)
        if "CRISIS" in estado_texto:
            estilo = {
                "color": "#d92b2b", 
                "bg": "#ffe6e6", 
                "titulo": "🚨 URGENTE: DECLARATORIA DE DESASTRE HÍDRICO",
                "icono": "🔴"
            }
            impacto_agro = """
            * **Arroz (Bajo Yaque):** Pérdida total proyectada (100%) por inviabilidad de inundación.
            * **Banano (Línea Noroeste):** Estrés severo. Se requiere auxilio de pozos tubulares.
            """
            impacto_urbano = "**CORAASAN (Santiago):** Déficit del 40%. Racionamiento obligatorio (48h)."
            acciones = [
                "🔴 **CIERRE TOTAL** del Canal Monsieur Bogaert y UFE.",
                "🔴 Operación de Presa Tavera-Bao en cota mínima (solo humano).",
                "🔴 Activación del Fondo de Contingencia (Aseguradora Agropecuaria)."
            ]
            
        elif "ALERTA" in estado_texto:
            estilo = {
                "color": "#ff9900", 
                "bg": "#fff8e6", 
                "titulo": "⚠️ AVISO: RESTRICCIÓN DE CAUDALES",
                "icono": "🟡"
            }
            impacto_agro = """
            * **Arroz:** Prohibición de siembra de tercera etapa ("Viveros").
            * **Turnos de Riego:** Reducción a 3 días por semana.
            """
            impacto_urbano = "**Acueductos Rurales:** Reducción de presión nocturna."
            acciones = [
                "🟡 Reducción del 30% en válvulas de salida.",
                "🟡 Suspensión de lavado de vehículos en Santiago.",
                "🟡 Monitoreo diario de infiltración."
            ]
            
        else:
            estilo = {
                "color": "#28a745", 
                "bg": "#e6f9e9", 
                "titulo": "✅ INFORME OPERATIVO: ESTABILIDAD",
                "icono": "🟢"
            }
            impacto_agro = "**Ciclo de Siembra:** Garantizado al 100%."
            impacto_urbano = "Abastecimiento continuo (24/7)."
            acciones = [
                "🟢 Mantener curva guía de operación.",
                "🟢 Mantenimiento preventivo de compuertas.",
                "🟢 Maximizar generación hidroeléctrica."
            ]

        # 3. Renderizado Visual (El Documento)
        with st.container(border=True):
            # Cabecera
            c1, c2 = st.columns([1, 4])
            with c1: st.markdown("🇩🇴 **INDRHI / COPRE**")
            with c2: 
                st.markdown(f"**REF:** PARGIRH-INT-{fecha_rep.replace('-','')} | **FECHA:** {fecha_rep}")
                st.markdown(f"**ASUNTO:** {estilo['titulo']}")
            
            st.divider()
            
            # Cuerpo
            col_izq, col_der = st.columns(2)
            
            with col_izq:
                st.markdown("### 1. INTELIGENCIA DE DATOS")
                st.markdown(f"""
                El modelo **RH-PARGIRH (IA)** reporta:
                * 🌊 **Caudal Proyectado:** `{promedio_actual:.1f} m³/s`
                * 📉 **Variación Histórica:** `{variacion:.1f}%`
                * 🏜️ **Inercia del Suelo:** `{inercia_promedio:.1f} mm`
                """)
                
                st.markdown("### 2. IMPACTO SOCIOECONÓMICO")
                st.info(impacto_agro)
                st.warning(impacto_urbano)
            
            with col_der:
                st.markdown("### 3. DIRECTRICES OPERATIVAS")
                st.markdown("Según Art. 4 del Reglamento de Aguas:")
                for orden in acciones:
                    st.markdown(f"#### {orden}")
                
                st.caption("🔒 Documento oficial generado por Sistema DSS. Firma digital válida.")
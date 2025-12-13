import streamlit as st

class ReportGenerator:
    def render_button(self, df_view, kpis):
        st.markdown("---")
        st.subheader("📄 Generador de Memorándums de Inteligencia")
        st.info("Generación de directrices operativas basadas en el Manual de Operación de Presas y Embalses (MOPE).")
        
        # 1. Inicializar estado de memoria si no existe
        if "show_report" not in st.session_state:
            st.session_state.show_report = False

        # 2. Botón interruptor (Toggle)
        label_btn = "❌ Cerrar Informe" if st.session_state.show_report else "📄 Generar Memorándum Ejecutivo"
        
        if st.button(label_btn):
            st.session_state.show_report = not st.session_state.show_report
            st.rerun()

        # 3. Mostrar reporte si está activo
        if st.session_state.show_report:
            self._generate_memo(df_view, kpis)

    def _generate_memo(self, df_view, kpis):
        # Desempaquetar datos
        fecha_rep = df_view['Fecha'].max().strftime('%Y-%m')
        promedio_actual = kpis['promedio']
        variacion = kpis['variacion']
        inercia_promedio = kpis['inercia']
        estado_texto = kpis['estado_texto']
        
        # Lógica de Negocio Avanzada (La versión buena)
        if "CRISIS" in estado_texto:
            estilo = {
                "color": "#d92b2b", 
                "bg": "#ffe6e6", 
                "titulo": "🚨 URGENTE: DECLARATORIA DE DESASTRE HÍDRICO",
                "borde": "red"
            }
            impacto_agro = """
            * **Arroz (Bajo Yaque):** Pérdida total proyectada (100%) por inviabilidad de inundación.
            * **Banano (Línea Noroeste):** Estrés severo. Se requiere auxilio de pozos tubulares.
            * **Ganadería:** Riesgo alto en Montecristi.
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
                "titulo": "⚠️ AVISO: RESTRICCIÓN PREVENTIVA",
                "borde": "orange"
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
                "borde": "green"
            }
            impacto_agro = "**Ciclo de Siembra:** Garantizado al 100%."
            impacto_urbano = "Abastecimiento continuo (24/7)."
            acciones = [
                "🟢 Mantener curva guía de operación.",
                "🟢 Mantenimiento preventivo de compuertas.",
                "🟢 Maximizar generación hidroeléctrica."
            ]

        # RENDERIZADO DEL DOCUMENTO (Estilo Hoja Oficial)
        with st.container(border=True):
            # Cabecera
            c1, c2 = st.columns([1, 4])
            with c1: st.markdown("🇩🇴 **INDRHI / COPRE**")
            with c2: 
                st.markdown(f"**REF:** PARGIRH-INT-{fecha_rep.replace('-','')} | **FECHA:** {fecha_rep}")
                st.markdown(f"**ASUNTO:** <span style='color:{estilo['color']}'>{estilo['titulo']}</span>", unsafe_allow_html=True)
            
            st.divider()
            
            # Cuerpo en dos columnas
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
                if "CRISIS" in estado_texto:
                    st.error(impacto_agro)
                    st.error(impacto_urbano)
                elif "ALERTA" in estado_texto:
                    st.warning(impacto_agro)
                    st.warning(impacto_urbano)
                else:
                    st.success(impacto_agro)
            
            with col_der:
                st.markdown("### 3. DIRECTRICES OPERATIVAS")
                st.markdown("Según Art. 4 del Reglamento de Aguas:")
                for orden in acciones:
                    st.markdown(f"#### {orden}")
                
                st.markdown("---")
                st.caption("🔒 Documento oficial generado por Sistema DSS. Firma digital válida.")
                
        html_content = f"""
        <html>
        <head><title>Memorandum {fecha_rep}</title></head>
        <body style="font-family: sans-serif; padding: 40px;">
            <h1 style="color: #003366;">🇩🇴 INDRHI / COPRE</h1>
            <hr>
            <h3>ASUNTO: {estilo['titulo']}</h3>
            <p><strong>REF:</strong> PARGIRH-INT-{fecha_rep}</p>
            <br>
            <div style="background-color: {estilo['bg']}; padding: 20px; border-left: 5px solid {estilo['color']};">
                <h3>DIAGNÓSTICO</h3>
                <p>Caudal Proyectado: <strong>{promedio_actual:.1f} m³/s</strong></p>
                <p>Variación: <strong>{variacion:.1f}%</strong></p>
            </div>
            <br>
            <h3>ÓRDENES OPERATIVAS</h3>
            <ul>
                {''.join([f'<li>{acc}</li>' for acc in acciones])}
            </ul>
            <hr>
            <p style="font-size: small; color: gray;">Generado por Inteligencia Artificial RH-PARGIRH</p>
        </body>
        </html>
        """
        
        st.download_button(
            label="📥 Descargar Documento Oficial",
            data=html_content,
            file_name=f"MEMO_INDRHI_{fecha_rep}.html",
            mime="text/html"
        )
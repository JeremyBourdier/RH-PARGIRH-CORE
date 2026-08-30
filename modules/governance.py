import streamlit as st
import pandas as pd
import datetime
import hmac
import os


def authenticate_operator(password, expected_password):
    """Return whether the supplied password authorizes operator actions."""
    if not expected_password or not password:
        return False
    return hmac.compare_digest(password, expected_password)

class GovernanceModule:
    def __init__(self):
        # Inicializar el registro de auditoría en la sesión si no existe
        if 'audit_log' not in st.session_state:
            st.session_state['audit_log'] = []

    def evaluar_escenario(self, kpis):
        """
        Motor Híbrido: Convierte datos técnicos (Caudal) en reglas normativas (MOPE).
        """
        caudal = kpis.get('caudal_promedio', 0)
        
        # REGLAS DEL MOPE (Simuladas para el Hackathon, ya luego integramos el manual completo que no seria tan dificil pero eso lo quiere hacer con el chatbot de AI tambien=
        if caudal < 25:
            return {
                "nivel": "EMERGENCIA ROJA",
                "accion": "CIERRE TOTAL DE RIEGO AGRÍCOLA",
                "prioridad": "Consumo Humano Exclusivo",
                "fundamento": "Art. 4 Reglamento de Aguas y Resolución INDRHI-2025",
                "color": "error",
                "impacto_social": {"Agro": 0, "Urbano": 100, "Energia": 20}
            }
        elif caudal < 40:
            return {
                "nivel": "ALERTA AMARILLA",
                "accion": "TANDEO (Turnos de 12 horas)",
                "prioridad": "Riego Restringido + Consumo Humano",
                "fundamento": "Protocolo de Sequía Estacional - Fase 2",
                "color": "warning",
                "impacto_social": {"Agro": 50, "Urbano": 90, "Energia": 60}
            }
        else:
            return {
                "nivel": "NORMALIDAD VERDE",
                "accion": "OPERACIÓN ESTÁNDAR",
                "prioridad": "Todos los sectores garantizados",
                "fundamento": "Manual de Operación de Presas (MOPE)",
                "color": "success",
                "impacto_social": {"Agro": 100, "Urbano": 100, "Energia": 100}
            }

    def render_audit_log(self):
        st.markdown("### 📜 Notario Digital (Audit Log)")
        st.caption("Registro inmutable de decisiones conforme a ISO-31000.")
        
        if len(st.session_state['audit_log']) > 0:
            df_log = pd.DataFrame(st.session_state['audit_log'])
            # Mostramos el log como una tabla limpia
            st.dataframe(
                df_log, 
                column_config={
                    "timestamp": "Hora",
                    "autoridad": "Responsable",
                    "accion": "Decisión Tomada",
                    "causa": "Justificación Técnica"
                },
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No hay decisiones registradas en esta sesión.")

    def render(self, kpis):
        st.header("⚖️ Gobernabilidad y Toma de Decisiones")
        st.markdown("Este módulo transforma la **Inteligencia de Datos** en **Actos Administrativos** transparentes.")
        
        col_left, col_right = st.columns([1, 1.5])
        
        # 1. EL MOTOR HÍBRIDO
        escenario = self.evaluar_escenario(kpis)
        
        with col_left:
            st.subheader("Estado Situacional (Normativo)")
            if escenario['color'] == 'error':
                st.error(f"🛑 {escenario['nivel']}")
            elif escenario['color'] == 'warning':
                st.warning(f"⚠️ {escenario['nivel']}")
            else:
                st.success(f"✅ {escenario['nivel']}")
            
            st.metric("Caudal Actual (Dato IA)", f"{kpis['caudal_promedio']:.1f} m³/s")
            
            with st.expander("🔍 Ver Fundamento Legal", expanded=True):
                st.markdown(f"**Medida Recomendada:** {escenario['accion']}")
                st.markdown(f"**Prioridad de Ley:** {escenario['prioridad']}")
                st.markdown(f"**Base Legal:** *{escenario['fundamento']}*")

            # Botón de Acción (Simulación de Firma Digital) solo lo puse como ejemplo chicos 
            st.divider()
            expected_password = os.environ.get("PARGIRH_OPERATOR_PASSWORD")
            if not expected_password:
                st.error("Las acciones operativas están deshabilitadas: falta configurar la credencial del operador.")
            else:
                operator_password = st.text_input("Contraseña del operador:", type="password")
                if authenticate_operator(operator_password, expected_password):
                    st.session_state["operator_authorized"] = True
                else:
                    st.session_state["operator_authorized"] = False

                autoridad = st.text_input("Firma del Funcionario Responsable:", value="Operador INDRHI - Turno A")

                if st.button("🗳️ EJECUTAR DECISIÓN Y REGISTRAR", disabled=not st.session_state["operator_authorized"]) and st.session_state["operator_authorized"]:
                    # Guardamos en el "Blockchain" (Session State)
                    nuevo_registro = {
                        "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
                        "autoridad": autoridad,
                        "accion": escenario['accion'],
                        "causa": f"Caudal a {kpis['caudal_promedio']:.1f} m³/s ({escenario['nivel']})"
                    }
                    st.session_state['audit_log'].insert(0, nuevo_registro) # El más reciente primero
                    st.success("Decisión registrada en el Libro Oficial Digital.")
                    st.balloons()

        # 2. MATRIZ DE CONFLICTO 
        with col_right:
            st.subheader("📊 Matriz de Impacto Social")
            st.caption("Niveles de satisfacción sectorial proyectados según la decisión.")
            
            impactos = escenario['impacto_social']
            
            # Gráfica de Barras de Progreso para simular satisfacción
            st.write(f"🌾 **Sector Agrícola (Juntas de Regantes):** {impactos['Agro']}%")
            st.progress(impactos['Agro'] / 100, text="Disponibilidad Hídrica")
            
            st.write(f"🏙️ **Sector Urbano (INAPA/CORAASAN):** {impactos['Urbano']}%")
            st.progress(impactos['Urbano'] / 100, text="Abastecimiento Acueductos")
            
            st.write(f"⚡ **Sector Energético (EGEHID):** {impactos['Energia']}%")
            st.progress(impactos['Energia'] / 100, text="Capacidad de Generación")
            
            if escenario['color'] == 'error':
                st.warning("⚠️ **ALERTA DE CONFLICTO:** Riesgo alto de protestas en sector agrícola.")

        st.divider()
        
        # 3. EL LOG
        self.render_audit_log()

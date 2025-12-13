import streamlit as st
import time

class LegalAssistant:
    def __init__(self):
        # Base de conocimiento (Igual que antes)
        self.knowledge_base = {
            "roja": "🚨 **Art. 45 (Fase Roja):**\n\nEn caso de déficit >50%:\n1. Prohibición total de riego agrícola.\n2. Prioridad absoluta a consumo humano.\n3. Control militar de válvulas si es necesario.",
            "amarilla": "⚠️ **Art. 44 (Fase Amarilla):**\n\nEn caso de déficit 30-50%:\n1. Riego restringido (2 días/sem).\n2. Prohibición de lavado de vehículos.\n3. Multas por desperdicio en zonas urbanas.",
            "inercia": "🌱 **Inercia Hídrica (Definición):**\n\nEs la memoria del suelo. Un valor bajo (<40mm) indica que el suelo está seco y absorberá la lluvia antes de que llegue al río. Es un indicador temprano de sequía invisible.",
            "ayuda": "Soy el **Asistente Legal PARGIRH**. Puedo citar el protocolo oficial.\n\nPregúntame sobre:\n- Protocolo Fase Roja\n- Medidas Fase Amarilla\n- ¿Qué es la Inercia?"
        }

    def _stream_text(self, text):
        """Efecto visual de escritura 'tipo máquina de escribir'"""
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.05) # Velocidad de escritura

    def get_response(self, prompt):
        prompt = prompt.lower()
        if "roja" in prompt or "crisis" in prompt: return self.knowledge_base["roja"]
        elif "amarilla" in prompt or "alerta" in prompt: return self.knowledge_base["amarilla"]
        elif "inercia" in prompt or "suelo" in prompt: return self.knowledge_base["inercia"]
        else: return "No encuentro esa referencia en el Manual. Intenta preguntar por 'Fase Roja', 'Amarilla' o 'Inercia'."

    def render(self):
        st.markdown("---")
        
        # Encabezado del Chat con botón de limpiar
        c1, c2 = st.sidebar.columns([4, 1])
        with c1: st.subheader("💬 Asistente IA")
        with c2: 
            if st.button("🗑️", help="Borrar chat"):
                st.session_state.messages = []
                st.rerun()

        # Inicializar historial
        if "messages" not in st.session_state:
            st.session_state.messages = [{"role": "assistant", "content": self.knowledge_base["ayuda"]}]

        # Contenedor del chat (Altura fija para que se vea ordenado)
        chat_container = st.sidebar.container(height=400)
        
        # Mostrar historial con AVATARES
        with chat_container:
            for msg in st.session_state.messages:
                # Iconos personalizados
                avatar = "🤖" if msg["role"] == "assistant" else "👤"
                st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

        # Input del usuario
        if prompt := st.sidebar.chat_input("Pregunta al manual...", key="chat_input"):
            # 1. Mostrar mensaje usuario inmediatamente
            st.session_state.messages.append({"role": "user", "content": prompt})
            chat_container.chat_message("user", avatar="👤").write(prompt)
            
            # 2. Pensar...
            response_text = self.get_response(prompt)
            
            # 3. Respuesta con efecto STREAMING (Escribiendo...)
            with chat_container:
                with st.chat_message("assistant", avatar="🤖"):
                    # Usamos write_stream para el efecto visual
                    st.write_stream(self._stream_text(response_text))
            
            # 4. Guardar en historial
            st.session_state.messages.append({"role": "assistant", "content": response_text})
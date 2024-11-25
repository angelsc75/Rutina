import streamlit as st
from core.prompt_manager import PromptManager
from core.llm_manager import LLMManager
from config.settings import AVAILABLE_PLATFORMS, APP_SETTINGS

def main():
    st.title(APP_SETTINGS["title"])
    st.write(APP_SETTINGS["description"])
    
    # Inputs del usuario
    platform = st.selectbox("Selecciona la plataforma", AVAILABLE_PLATFORMS)
    tema = st.text_input("¿Sobre qué tema quieres generar contenido?")
    audiencia = st.text_input("¿Cuál es tu audiencia objetivo?")
    
    if st.button("Generar Contenido"):
        prompt_manager = PromptManager()
        llm_manager = LLMManager()
        
        prompt = prompt_manager.get_prompt(platform, tema, audiencia)
        contenido = llm_manager.generate_content(prompt)
        
        st.write("### Contenido Generado")
        st.write(contenido)

if __name__ == "__main__":
    main()
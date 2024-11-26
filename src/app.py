import streamlit as st
from core.prompt_manager import PromptManager
from core.llm_manager import LLMManager
from models.content import ContentManager
from config.settings import AVAILABLE_PLATFORMS, APP_SETTINGS
from core.image_generator import ImageGenerator
# Inicializar gestor de contenidos (podría ser global o en sesión)
content_manager = ContentManager()

def main():
    st.title(APP_SETTINGS["title"])
    st.write(APP_SETTINGS["description"])
    
    # Selector de proveedor LLM
    llm_provider = st.selectbox("Elige el proveedor de LLM", ['openai', 'groq'])
    
    # Inputs del usuario
    platform = st.selectbox("Selecciona la plataforma", AVAILABLE_PLATFORMS)
    tema = st.text_input("¿Sobre qué tema quieres generar contenido?")
    audiencia = st.text_input("¿Cuál es tu audiencia objetivo?")
    
    if st.button("Generar Contenido"):
        
        # Generación de texto
        prompt_manager = PromptManager()
        llm_manager = LLMManager(provider=llm_provider)
        
        
        
        
        
        # Obtener prompt específico
        prompt = prompt_manager.get_prompt(platform, tema, audiencia)
        
        # Generar contenido
        content = llm_manager.generate_content(prompt, platform, tema, audiencia)
        
        # Generación de imagen
        image_generator = ImageGenerator()
        image_prompt = f"Imagen representativa de {tema} para {platform}"
        imagen = image_generator.generate_image(image_prompt)
        
        if content:
            # Añadir a gestor de contenidos
            content_manager.add_content(content)
            
            # Mostrar contenido
            st.write("### Contenido Generado")
            st.write(content.text)
            
            # Mostrar detalles adicionales
            st.write("#### Detalles")
            st.write(f"**Plataforma:** {content.platform}")
            st.write(f"**Tema:** {content.topic}")
            st.write(f"**Audiencia:** {content.audience}")
            st.write(f"**Generado el:** {content.generated_at}")
        else:
            st.error("Hubo un problema generando el contenido")

if __name__ == "__main__":
    main()
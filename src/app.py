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
    
    # Checkbox para generar imagen
    generar_imagen = st.checkbox("Generar imagen para la publicación")
    
    if st.button("Generar Contenido"):
        # Generación de texto
        prompt_manager = PromptManager()
        llm_manager = LLMManager(provider=llm_provider)
        
        # Obtener prompt específico
        prompt = prompt_manager.get_prompt(platform, tema, audiencia)
        
        # Generar contenido
        content = llm_manager.generate_content(prompt, platform, tema, audiencia)
        
        # Generación de imagen condicional
        imagen = None
        
    # En la sección de generación de imagen
    if generar_imagen:
        # Mostrar un mensaje de carga
        with st.spinner('Generando imagen...'):
            image_generator = ImageGenerator()
        
            image_prompts = {
                "blog": f"Ilustración profesional que represente {tema}, estilo de imagen de blog de alta calidad",
                "twitter": f"Imagen cuadrada llamativa y concisa sobre {tema}, estilo de infografía para twitter",
                "instagram": f"Imagen visualmente atractiva de {tema}, estilo de post de Instagram con colores vibrantes",
                "linkedin": f"Imagen profesional corporativa relacionada con {tema}, estilo de contenido de LinkedIn"
            }
        
            image_prompt = image_prompts.get(platform, f"Imagen representativa de {tema}")
        
            imagen = image_generator.generate_image(image_prompt, platform)
        
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
            
            # Mostrar imagen si se generó
            if imagen and generar_imagen:
                st.write("### Imagen Generada")
                st.image(imagen, caption=f"Imagen para {platform}")
        else:
            st.error("Hubo un problema generando el contenido")

if __name__ == "__main__":
    main()
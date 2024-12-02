import streamlit as st
from core.prompt_manager import PromptManager
from core.llm_manager import LLMManager
from core.financial_news_generator import FinancialNewsGenerator
from core.scientific_rag import ScientificContentRAG
from core.image_generator import ImageGenerator
from config.settings import AVAILABLE_PLATFORMS, APP_SETTINGS, LLM_PROVIDERS

def main():
    st.title(APP_SETTINGS["title"])
    
    # Primer paso: Selección de idioma
    idioma = st.sidebar.radio("Selecciona Idioma", [
        "castellano", "english", "français", "italiano"
    ])
    
    # Segundo paso: Selección de aplicación
    aplicacion = st.sidebar.radio("Selecciona Aplicación", [
        "Generar Contenido por Plataforma", 
        "Información Financiera", 
        "Contenido Científico"
    ])
    
    # Selector de proveedor LLM
    llm_provider = st.sidebar.selectbox("Proveedor LLM", list(LLM_PROVIDERS.keys()))
    
    # Flujo principal basado en la aplicación seleccionada
    if aplicacion == "Generar Contenido por Plataforma":
        generar_contenido_por_plataforma(idioma, llm_provider)
    
    elif aplicacion == "Información Financiera":
        informacion_financiera(llm_provider)
    
    elif aplicacion == "Contenido Científico":
        contenido_cientifico(idioma, llm_provider)

def generar_contenido_por_plataforma(idioma, llm_provider):
    # Selección de plataforma
    platform = st.selectbox("Selecciona la plataforma", AVAILABLE_PLATFORMS)
    
    # Tema y audiencia
    tema = st.text_input("¿Sobre qué tema quieres generar contenido?")
    audiencia = st.text_input("¿Cuál es tu audiencia objetivo?")
    
    # Checkbox para generación de imagen
    generar_imagen = st.checkbox("¿Quieres generar una imagen para acompañar el contenido?")
    
    # Opciones de imagen (solo si el checkbox está marcado)
    image_generator = None
    image_prompt = None
    if generar_imagen:
        # Opciones de generación de imagen
        image_source = st.radio("Selecciona fuente de imagen", [
            "Generar con IA", 
            "Buscar en Unsplash"
        ])
        
        # Selector de generador de IA
        if image_source == "Generar con IA":
            generator = st.selectbox("Selecciona generador de IA", [
                'stable-diffusion', 
                'dall-e'
            ])
        else:
            generator = 'unsplash'
        
        # Prompt para imagen 
        image_prompt = st.text_input(
            "Descripción de la imagen (opcional)", 
            value=tema
        )
    
    # Botón de generación de contenido
    if st.button("Generar Contenido"):
        # Generar contenido de texto
        prompt_manager = PromptManager()
        llm_manager = LLMManager(provider=llm_provider)
        
        prompt = prompt_manager.get_prompt(
            platform, tema, audiencia, 
            idioma=idioma
        )
        
        content = llm_manager.generate_content(
            prompt, platform, tema, audiencia
        )
        
        st.write(f"### Contenido en {idioma.capitalize()}")
        st.write(content.text)
        
        # Generación de imagen si está marcado el checkbox
        if generar_imagen:
            st.subheader("Imagen Generada")
            
            # Inicializar generador de imágenes
            image_generator = ImageGenerator()
            
            # Generar o buscar imagen
            image = image_generator.generate_image(
                image_prompt or tema, 
                platform, 
                generator
            )
            
            if image:
                st.image(image, caption=image_prompt or tema)
            else:
                st.error("No se pudo generar/encontrar la imagen")

def informacion_financiera(llm_provider):
    st.header("Noticias Financieras por Mercado")

    financial_generator = FinancialNewsGenerator()

    # Selector de mercado
    market_tickers = {
        "S&P 500": "^GSPC",
        "NASDAQ Composite": "^IXIC",
        "Dow Jones": "^DJI",
        "FTSE 100": "^FTSE",
        "Nikkei 225": "^N225"
    }
    selected_market = st.selectbox("Selecciona un Mercado", list(market_tickers.keys()))

    if st.button("Mostrar Informe del Mercado"):
        try:
            market_ticker = market_tickers[selected_market]
            report = financial_generator.generate_market_report(market_ticker, top_n=5)
            st.text(report)
        except Exception as e:
            st.error(f"Error al generar el informe: {e}")

def contenido_cientifico(idioma, llm_provider):
    st.header("Contenido Científico Divulgativo")
    
    dominio = st.selectbox("Área Científica", [
        "física cuántica", 
        "inteligencia artificial", 
        "biomedicina", 
        "astrofísica"
    ])
    
    consulta = st.text_input("Consulta científica específica")
    
    if st.button("Generar Contenido Científico"):
        scientific_rag = ScientificContentRAG(
            domain=dominio, 
            language=idioma
        )
        
        content = scientific_rag.generate_scientific_content(consulta)
        
        st.write(f"### Contenido Científico en {idioma.capitalize()}")
        st.write(content.text)
        
        with st.expander("Referencias Científicas"):
            papers = scientific_rag.fetch_arxiv_papers()
            for paper in papers:
                st.write(f"**{paper['title']}**")
                st.write(paper['summary'])

if __name__ == "__main__":
    main()
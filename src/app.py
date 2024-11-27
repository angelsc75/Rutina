import streamlit as st
from core.prompt_manager import PromptManager
from core.llm_manager import LLMManager
from core.financial_news_generator import FinancialNewsGenerator  # Nuevo
from core.scientific_rag import ScientificContentRAG  # Nuevo
from models.content import ContentManager
from config.settings import AVAILABLE_PLATFORMS, APP_SETTINGS, LLM_PROVIDERS

def main():
    st.title(APP_SETTINGS["title"])
    st.sidebar.title("Opciones Avanzadas")

    # Menú de funcionalidades avanzadas
    feature_mode = st.sidebar.radio("Selecciona Modo", [
        "Generación Estándar", 
        "Contenido Multilingüe", 
        "Noticias Financieras", 
        "Contenido Científico"
    ])

    # Selector de proveedor LLM
    llm_provider = st.sidebar.selectbox("Proveedor LLM", list(LLM_PROVIDERS.keys()))

    if feature_mode == "Generación Estándar":
        standard_content_generation(llm_provider)
    
    elif feature_mode == "Contenido Multilingüe":
        multilingual_content_generation(llm_provider)
    
    elif feature_mode == "Noticias Financieras":
        financial_news_generation(llm_provider)
    
    elif feature_mode == "Contenido Científico":
        scientific_content_generation(llm_provider)

def standard_content_generation(llm_provider):
    # Lógica actual de generación de contenido
    platform = st.selectbox("Selecciona la plataforma", AVAILABLE_PLATFORMS)
    tema = st.text_input("¿Sobre qué tema quieres generar contenido?")
    audiencia = st.text_input("¿Cuál es tu audiencia objetivo?")
    
    # Resto del código de generación estándar...

def multilingual_content_generation(llm_provider):
    st.header("Generación de Contenido Multilingüe")
    
    # Selector de idioma
    idioma = st.selectbox("Selecciona Idioma", [
        "castellano", "english", "français", "italiano"
    ])
    
    # Campos similares a generación estándar
    platform = st.selectbox("Plataforma", AVAILABLE_PLATFORMS)
    tema = st.text_input("Tema del contenido")
    audiencia = st.text_input("Audiencia objetivo")
    
    if st.button("Generar Contenido Multilingüe"):
        prompt_manager = PromptManager()
        llm_manager = LLMManager(provider=llm_provider)
        
        # Generar con parámetro de idioma
        prompt = prompt_manager.get_prompt(
            platform, tema, audiencia, 
            idioma=idioma
        )
        
        content = llm_manager.generate_content(
            prompt, platform, tema, audiencia
        )
        
        st.write(f"### Contenido en {idioma.capitalize()}")
        st.write(content.text)

def financial_news_generation(llm_provider):
    st.header("Noticias de Mercados Financieros")
    
    # Selector de categoría de noticias
    categoria = st.selectbox("Categoría", [
        "technology", "finance", "economy", "markets"
    ])
    
    # Selector de plataforma para formato
    platform = st.selectbox("Formato de Publicación", AVAILABLE_PLATFORMS)
    
    if st.button("Generar Informe Financiero"):
        financial_generator = FinancialNewsGenerator(
            api_key=os.getenv("ALPHA_VANTAGE_KEY")
        )
        
        # Obtener noticias
        news_data = financial_generator.get_market_news(categoria)
        
        # Generar contenido
        content = financial_generator.generate_financial_content(news_data)
        
        st.write("### Informe Financiero")
        st.write(content.text)

def scientific_content_generation(llm_provider):
    st.header("Contenido Científico Divulgativo")
    
    # Selector de dominio científico
    dominio = st.selectbox("Área Científica", [
        "física cuántica", 
        "inteligencia artificial", 
        "biomedicina", 
        "astrofísica"
    ])
    
    # Input de consulta específica
    consulta = st.text_input("Consulta científica específica")
    
    # Selector de plataforma
    platform = st.selectbox("Formato de Publicación", AVAILABLE_PLATFORMS)
    
    if st.button("Generar Contenido Científico"):
        scientific_rag = ScientificContentRAG(domain=dominio)
        
        # Generar contenido con RAG
        content = scientific_rag.generate_scientific_content(consulta)
        
        st.write("### Contenido Científico Divulgativo")
        st.write(content.text)
        
        # Mostrar papers de referencia
        with st.expander("Referencias Científicas"):
            papers = scientific_rag.fetch_arxiv_papers()
            for paper in papers:
                st.write(f"**{paper['title']}**")
                st.write(paper['summary'])

if __name__ == "__main__":
    main()
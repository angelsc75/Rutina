import streamlit as st
from core.prompt_manager import PromptManager
from core.llm_manager import LLMManager
from core.financial_news_generator import FinancialNewsGenerator  # Nuevo
from core.scientific_rag import ScientificContentRAG  # Nuevo
from models.content import ContentManager
from config.settings import AVAILABLE_PLATFORMS, APP_SETTINGS, LLM_PROVIDERS
import os
def main():
    st.title(APP_SETTINGS["title"])
    st.sidebar.title("Opciones Avanzadas")

    # Menú de funcionalidades avanzadas
    feature_mode = st.sidebar.radio("Selecciona Modo", [
        "Generación Estándar", 
        "Noticias Financieras", 
        "Contenido Científico"
    ])

    # Selector de proveedor LLM
    llm_provider = st.sidebar.selectbox("Proveedor LLM", list(LLM_PROVIDERS.keys()))

    if feature_mode == "Generación Estándar":
        standard_content_generation(llm_provider)
    
    elif feature_mode == "Noticias Financieras":
        financial_news_generation(llm_provider)
    
    elif feature_mode == "Contenido Científico":
        scientific_content_generation(llm_provider)

def standard_content_generation(llm_provider):
    # Selector de idioma
    idioma = st.selectbox("Selecciona Idioma", [
        "castellano", "english", "français", "italiano"
    ])
    
    platform = st.selectbox("Selecciona la plataforma", AVAILABLE_PLATFORMS)
    tema = st.text_input("¿Sobre qué tema quieres generar contenido?")
    audiencia = st.text_input("¿Cuál es tu audiencia objetivo?")
    
    if st.button("Generar Contenido"):
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
    
    # Resto del código de generación estándar...



def financial_news_generation(llm_provider):
    st.header("Noticias de Mercados Financieros")
    
    # Selector de idioma
    idioma = st.selectbox("Selecciona Idioma", [
        "castellano", "english", "français", "italiano"
    ])
    
    categoria = st.selectbox("Categoría", [
        "technology", "finance", "economy", "markets"
    ])
    
    platform = st.selectbox("Formato de Publicación", AVAILABLE_PLATFORMS)
    
    if st.button("Generar Informe Financiero"):
        financial_generator = FinancialNewsGenerator(
            api_key=os.getenv("ALPHA_VANTAGE_KEY")
        )
        
        news_data = financial_generator.get_market_news(categoria)
        
        # Generar contenido con el idioma seleccionado
        content = financial_generator.generate_financial_content(
            news_data, 
            language=idioma
        )
        
        st.write(f"### Informe Financiero en {idioma.capitalize()}")
        st.write(content.text)

def scientific_content_generation(llm_provider):
    st.header("Contenido Científico Divulgativo")
    
    # Selector de idioma
    idioma = st.selectbox("Selecciona Idioma", [
        "castellano", "english", "français", "italiano"
    ])
    
    dominio = st.selectbox("Área Científica", [
        "física cuántica", 
        "inteligencia artificial", 
        "biomedicina", 
        "astrofísica"
    ])
    
    consulta = st.text_input("Consulta científica específica")
    
    platform = st.selectbox("Formato de Publicación", AVAILABLE_PLATFORMS)
    
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
import streamlit as st
from core.prompt_manager import PromptManager
from core.llm_manager import LLMManager
from core.financial_news_generator import FinancialNewsGenerator
from core.scientific_rag import ScientificContentRAG
from core.image_generator import ImageGenerator
from config.settings import AVAILABLE_PLATFORMS, APP_SETTINGS, LLM_PROVIDERS
import plotly.graph_objs as plt
import yfinance as yf
from core.sientific_agents import MultiAgentSystem

def main():
    st.title(APP_SETTINGS["title"])
    
    # Primer paso: Selección de idioma
    idioma = st.sidebar.radio("Selecciona Idioma", [
        "castellano", "english", "français", "italiano"
    ], key="main_language_selector")
    
    # Segundo paso: Selección de aplicación
    aplicacion = st.sidebar.radio("Selecciona Aplicación", [
        "Generar Contenido por Plataforma", 
        "Información Financiera", 
        "Contenido Científico"
    ], key="app_selector")
    
    # Selector de proveedor LLM
    llm_provider = st.sidebar.selectbox("Proveedor LLM", list(LLM_PROVIDERS.keys()))
    
    # Flujo principal basado en la aplicación seleccionada
    if aplicacion == "Generar Contenido por Plataforma":
        generar_contenido_por_plataforma(idioma, llm_provider)
    
    elif aplicacion == "Información Financiera":
        informacion_financiera(idioma,llm_provider)
    
    elif aplicacion == "Contenido Científico":
        contenido_cientifico(idioma,llm_provider)

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

def informacion_financiera(idioma, llm_provider):  # Recibe el idioma como parámetro
    st.header("Noticias Financieras por Mercado")

    financial_generator = FinancialNewsGenerator()

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
            
            # Obtener datos de mercado y acciones
            market_performance = financial_generator.get_market_performance(market_ticker)
            top_stocks = financial_generator.get_top_stocks_from_market(market_ticker, top_n=5)
            
            # Mostrar información general del mercado
            if market_performance:
                st.subheader(f"Rendimiento de {selected_market}")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Precio Actual", f"${market_performance['current_price']:.2f}")
                with col2:
                    st.metric("Cambio", f"${market_performance['change']:.2f}", 
                              f"{market_performance['change_percent']:.2f}%")
                with col3:
                    st.metric("Tendencia", 
                              "Positiva" if market_performance['change'] > 0 else "Negativa")
            
            # Mostrar información de acciones
            st.subheader("Acciones Destacadas")
            cols = st.columns(5)
            
            for i, stock in enumerate(top_stocks):
                with cols[i]:
                    with st.container(border=True):
                        st.markdown(f"**{stock['name']}**")
                        st.markdown(f"Símbolo: `{stock['symbol']}`")
                        st.markdown(f"Precio: **${stock['price']:.2f}**")
                        
                        # Colorear el cambio según sea positivo o negativo
                        if stock['change'] >= 0:
                            st.markdown(f"Cambio: :green[+${stock['change']:.2f}]")
                            st.markdown(f"Cambio %: :green[+{stock['change_percent']:.2f}%]")
                        else:
                            st.markdown(f"Cambio: :red[${stock['change']:.2f}]")
                            st.markdown(f"Cambio %: :red[{stock['change_percent']:.2f}%]")
            
            # Fetch and display financial news
            st.subheader("Noticias Financieras Recientes")
            
            # Fetch news related to the selected market and language
            news_articles = financial_generator.get_financial_news(selected_market, language=idioma)
            
            if news_articles:
                for article in news_articles:
                    with st.expander(article['title']):
                        st.write(article['description'])
                        st.markdown(f"**Fuente:** {article['source']}")
                        st.markdown(f"[Leer más]({article['url']})")
            else:
                st.warning(f"No se encontraron noticias recientes para {selected_market}.")
                st.info("Posibles razones:\n"
                        "- Límite de solicitudes alcanzado\n"
                        "- Problemas de conexión\n"
                        "- Sin noticias disponibles en este momento")
            
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
    simplificacion = st.checkbox("Simplificar para público general")
    
    if st.button("Generar Contenido Científico"):
        # Validar que se haya ingresado una consulta
        if not consulta:
            st.warning("Por favor, ingrese una consulta científica.")
            return
        
        # Inicializar sistema multiagente
        agent_system = MultiAgentSystem(language=idioma, llm_provider=llm_provider)
        
        # Realizar consultas y simplificaciones
        retrieval_result = agent_system.dispatch("retrieval", consulta)
        
        if retrieval_result is None or "Error" in str(retrieval_result):
            st.error(f"Error al recuperar contenido científico: {retrieval_result}")
            return
        
        if simplificacion:
            simplified_content = agent_system.dispatch("simplification", retrieval_result)
            if simplified_content is None or "Error" in str(simplified_content):
                st.error(f"Error al simplificar contenido: {simplified_content}")
                return
        else:
            simplified_content = retrieval_result
        
        enriched_content = agent_system.dispatch("graph_enrichment", simplified_content)
        
        if enriched_content is None or "Error" in str(enriched_content):
            st.error(f"Error al enriquecer contenido: {enriched_content}")
            return
        
        # Mostrar resultados
        st.write(f"### Contenido Científico en {idioma.capitalize()}")
        st.write(enriched_content)


if __name__ == "__main__":
    main()
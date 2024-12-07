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
from core.scientific_rag import ScientificContentRAG

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
        "Contenido Científico",
        "Contenido Científico con Grafos",
        "Artículo de Medium"  # Nueva opción
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
    
    elif aplicacion == "Contenido Científico con Grafos":
        contenido_cientifico_con_grafos(idioma, llm_provider)
    
    elif aplicacion == "Artículo de Medium":
        generar_articulo_medium(idioma, llm_provider)

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
     # Validaciones y selección más robustas
    dominio = st.selectbox("Área Científica", [
        "física cuántica", 
        "inteligencia artificial", 
        "biomedicina", 
        "astrofísica"
    ])
    
    consulta = st.text_input("Consulta científica específica")
    
    if st.button("Generar Contenido Científico"):
        if not consulta:
            st.warning("Por favor, ingrese una consulta científica.")
            return
        
        rag_system = ScientificContentRAG(
            domain=dominio, 
            language=idioma, 
            provider=llm_provider
        )
        
        try:
            result = rag_system.generate_scientific_graph_report(consulta)
            
            # Mostrar contenido científico
            st.write(result['scientific_content'])
            
            # Mostrar papers usados
            st.subheader("Papers Científicos Utilizados")
            for paper in result['papers']:
                with st.expander(paper['title']):
                    st.write(f"**Resumen:** {paper['summary']}")
                    st.write(f"**Autores:** {', '.join(paper['authors'])}")
                    st.markdown(f"[Enlace al paper]({paper['url']})")
        
        except Exception as e:
            st.error(f"Error en generación de contenido: {e}")

def contenido_cientifico_con_grafos(idioma, llm_provider):
    st.header("Generación de Contenido Científico con Grafos")
    
    # Mismos dominios que en contenido_cientifico
    dominio = st.selectbox("Área Científica", [
        "física cuántica", 
        "inteligencia artificial", 
        "biomedicina", 
        "astrofísica"
    ])
    
    consulta = st.text_input("Consulta científica específica")
    
    # Opciones adicionales para Graph RAG
    mostrar_grafo = st.checkbox("Mostrar relaciones del grafo de conocimiento")
    max_papers = st.slider("Número máximo de papers", 1, 20, 5)
    
    if st.button("Generar Contenido con Grafos"):
        if not consulta:
            st.warning("Por favor, ingrese una consulta científica.")
            return
        
        # Inicializar ScientificContentRAG
        rag_system = ScientificContentRAG(domain=dominio, language=idioma)
        
        try:
            # Generar informe científico
            result = rag_system.generate_scientific_graph_report(consulta)
            
            # Mostrar papers recuperados
            st.subheader("Papers Científicos Recuperados")
            for paper in result['papers'][:max_papers]:
                with st.expander(paper['title']):
                    st.write(f"**Resumen:** {paper['summary']}")
                    st.write(f"**Autores:** {', '.join(paper['authors'])}")
                    st.markdown(f"[Enlace al paper]({paper['url']})")
            
            # Mostrar enriquecimiento de grafo si está habilitado
            if mostrar_grafo:
                st.subheader("Relaciones de Conocimiento")
                for rel in result['graph_enrichment']:
                    st.markdown(f"""
                    - **{rel['source_concept']}** 
                    *{rel['relation']}* 
                    **{rel['target_concept']}**
                    """)
        
        except Exception as e:
            st.error(f"Error en generación de contenido: {e}")
            
def generar_articulo_medium(idioma, llm_provider):
    st.header("Generate Comprehensive Medium Article")
    
    # Input para el título del artículo
    article_title = st.text_input(
        "What is the title of your article?", 
        placeholder="e.g., 'Mindful Machines: Transforming Creative Stress through Intelligent Automation'"
    )
    
    # Input para el nombre de la aplicación
    app_name = st.text_input(
        "What is the name of your application?", 
        placeholder="e.g., ContentCraft AI, SmartContent Generator"
    )
    
    if not article_title or not app_name:
        st.warning("Please provide both an article title and application name.")
        return
    
    # Recopilar archivos del proyecto para incluir en el artículo
    archivos_proyecto = [
        "src/app.py", 
        "src/core/llm_manager.py", 
        "src/core/prompt_manager.py", 
        "src/core/financial_news_generator.py",
        "src/core/scientific_rag.py"
    ]
    
    codigos_proyecto = {}
    for archivo in archivos_proyecto:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                codigos_proyecto[archivo] = f.read()
        except Exception as e:
            st.warning(f"Could not read {archivo}: {e}")
    
    # Preparar códigos para incluir en el artículo
    codigo_completo = "\n\n---\n\n".join([
        f"## Code for {archivo}\n```python\n{codigo}\n```" 
        for archivo, codigo in codigos_proyecto.items()
    ])
    
    if st.button("Generate Medium Article"):
        # Inicializar managers
        prompt_manager = PromptManager()
        llm_manager = LLMManager(provider=llm_provider)
        
        # Generar prompt para Medium
        prompt = prompt_manager.get_prompt(
            "medium", 
            "AI, Mental Health, and Content Creation", 
            "Professionals and technology enthusiasts", 
            idioma=idioma,
            article_title=article_title,
            app_name=app_name
        )
        
        # Añadir códigos al final del prompt
        prompt_con_codigo = f"{prompt}\n\n## Detailed Code Components\n\n{codigo_completo}"
        
        # Generar contenido
        content = llm_manager.generate_content(
            prompt_con_codigo, 
            "medium", 
            f"Comprehensive Analysis of {app_name}", 
            "Tech developers"
        )
        
        st.write("### Generated Medium Article")
        st.write(content.text)
        
        # Opción de guardar artículo
        st.download_button(
            label="Download Article",
            data=content.text,
            file_name=f"{article_title.replace(' ', '_')}_medium_article.md",
            mime="text/markdown"
        )            
            
if __name__ == "__main__":
    main()
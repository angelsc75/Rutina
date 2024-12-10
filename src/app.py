from datetime import datetime
import graphviz
import streamlit as st
from core.prompt_manager import PromptManager
from core.llm_manager import LLMManager
from core.financial_news_generator import FinancialNewsGenerator
from core.scientific_rag import ScientificContentRAG
from core.image_generator import ImageGenerator
from config.settings import AVAILABLE_PLATFORMS, APP_SETTINGS, LLM_PROVIDERS
import plotly.graph_objs as plt
import yfinance as yf
from core.scientific_rag import ScientificContentRAG
import io
import zipfile
from langsmith import Client, traceable
import os
from dotenv import load_dotenv

def main():
    st.set_page_config(
        page_title="Rutina",
        page_icon="🔍",
        layout="wide"
    )
 # Añadir estilo para fondo blanco del sidebar
    st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.sidebar.columns([1,2,1])
    
    with col2:
        st.image("src/images/rutina_logo_baja.png")
    
    # Añadir título grande de la aplicación
    st.title("Rutina: Generación de Contenido Inteligente")
    
    # Primer paso: Selección de idioma
    idioma = st.sidebar.radio("Selecciona Idioma", [
        "castellano", "english", "français", "italiano"
    ], key="main_language_selector")
    
    # Segundo paso: Selección de aplicación
    aplicacion = st.sidebar.radio("Selecciona Aplicación", [
        "Generar Contenido por Plataforma", 
        "Información Financiera", 
        "Contenido Científico",
         "Artículo de Medium",
        "Funcionalidades Desarrollador"  # Nueva opción
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
    
    elif aplicacion == "Artículo de Medium":
        generar_articulo_medium(idioma, llm_provider)
    
    elif aplicacion == "Funcionalidades Desarrollador":
        generar_recursos_desarrollador(idioma, llm_provider)

def generar_contenido_por_plataforma(idioma, llm_provider):
    st.header("Generar contenido para plataformas")
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
            "Buscar en Unsplash",
            "Buscar en Pixabay"  # Nueva opción
        ])
        
        # Selector de generador de IA
        if image_source == "Generar con IA":
            generator = st.selectbox("Selecciona generador de IA", [
                'stable-diffusion', 
                'dall-e'
            ])
        elif image_source == "Buscar en Unsplash":
            generator = 'unsplash'
        else:  # Pixabay
            generator = 'pixabay'
        
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
            st.subheader("Imagen")
            
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
    "S&P 500 (Bolsa de Nueva York, EE.UU.)": "^GSPC",
    "NASDAQ Composite (Bolsa de Nasdaq, EE.UU.)": "^IXIC", 
    "Dow Jones (Bolsa de Nueva York, EE.UU.)": "^DJI",
    "FTSE 100 (Bolsa de Londres, Reino Unido)": "^FTSE",
    "Nikkei 225 (Bolsa de Tokio, Japón)": "^N225"
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
    st.header("Contenido Científico")
    
    # Selector de dominio científico
    dominio = st.selectbox("Área Científica", [
        "física cuántica", 
        "inteligencia artificial", 
        "biomedicina", 
        "astrofísica",
        "neurociencia", 
        "biología molecular", 
        "cambio climático", 
        "genética", 
        "nanotecnología", 
        "robótica", 
        "computación cuántica"
    ])
    
    # Consulta científica
    consulta = st.text_input("Consulta científica específica")
    
    # Checkbox para mostrar grafos de conocimiento
    mostrar_grafo = st.checkbox("Mostrar grafo de relaciones científicas")
    
    # Opciones adicionales para Graph RAG
    max_papers = st.slider("Número máximo de papers", 1, 20, 5)
    
    if st.button("Generar Contenido Científico"):
        if not consulta:
            st.warning("Por favor, ingrese una consulta científica.")
            return
        
        # Inicializar ScientificContentRAG
        rag_system = ScientificContentRAG(
            domain=dominio, 
            language=idioma, 
            provider=llm_provider,
            max_papers=max_papers
        )
        
        try:
            # Generar informe científico con papers y posible grafo
            result = rag_system.generate_scientific_graph_report(consulta)
            
            # Mostrar contenido científico
            st.subheader("Contenido Científico Generado")
            st.write(result['scientific_content'])
            
            # Mostrar papers recuperados
            st.subheader("Papers Científicos Recuperados")
            for paper in result['papers'][:max_papers]:
                with st.expander(paper['title']):
                    st.write(f"**Resumen:** {paper['summary']}")
                    st.write(f"**Autores:** {', '.join(paper['authors'])}")
                    st.markdown(f"[Enlace al paper]({paper['url']})")
            
            # Mostrar grafo si está habilitado y existe
            if mostrar_grafo and result.get('graph_enrichment'):
                st.subheader("Grafo de Relaciones Científicas")
                
                # Crear grafo con Graphviz
                dot = graphviz.Digraph(comment='Grafo de Conocimiento Científico')
                dot.attr(rankdir='LR')  # De izquierda a derecha
                
                # Añadir nodos y aristas
                for rel in result['graph_enrichment']:
                    source = str(rel.get('source_concept', 'Concepto Fuente'))
                    target = str(rel.get('target_concept', 'Concepto Destino'))
                    relation = rel.get('relation', 'Relación')
                    
                    # Añadir nodos
                    dot.node(source, source, shape='box')
                    dot.node(target, target, shape='box')
                    
                    # Añadir arista con etiqueta de relación
                    dot.edge(source, target, label=relation)
                
                # Renderizar grafo en Streamlit
                st.graphviz_chart(dot)
                
                # Mostrar detalles adicionales de las relaciones
                st.subheader("Detalles de Relaciones")
                for rel in result['graph_enrichment']:
                    st.markdown(f"""
                    ### Relación: {rel.get('source_concept', 'N/A')} → {rel.get('target_concept', 'N/A')}
                    - **Tipo de Relación:** {rel.get('relation', 'No especificado')}
                    - **Significancia:** {rel.get('significance', 'No evaluada')}
                    - **Implicaciones:** {rel.get('implications', 'Sin detalles adicionales')}
                    - **Nivel de Confianza:** {rel.get('confidence_level', 'No determinado')}
                    """)
        
        except Exception as e:
            st.error(f"Error en generación de contenido: {e}")
            
def generar_articulo_medium(idioma, llm_provider):
    st.warning("⚠️ Importante: Para generar artículos de Medium, se utilizará:\n- Proveedor LLM: OpenAI\n- Idioma: Castellano")
    
    # Forzar OpenAI y castellano
    llm_provider = 'openai'
    idioma = 'castellano'
    
    st.header("Generar Artículo Completo de Medium")
    
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
    
    # Validar longitud del título
    if len(article_title) < 10:
        st.warning("El título debe tener al menos 10 caracteres.")
        return
    
    if not app_name:
        st.warning("Please provide an application name.")
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
            article_title,  # Usar el título proporcionado como tema
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
            article_title,  # Usar el título proporcionado 
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

def generar_recursos_desarrollador(idioma, llm_provider):
    st.warning("⚠️ Importante: Para generar archivos para desarrolladores, se utilizará:\n- Proveedor LLM: OpenAI\n- Idioma: Castellano")
    
    # Forzar OpenAI y castellano
    llm_provider = 'openai'
    idioma = 'castellano'
    st.header("Recursos para Desarrolladores")
    st.subheader("requirements, readme y dockerfile")
    
    
    
    # Recopilar archivos del proyecto para análisis
    archivos_proyecto = [
        "src/app.py", 
        "src/core/llm_manager.py", 
        "src/core/prompt_manager.py", 
        "src/core/financial_news_generator.py",
        "src/core/scientific_rag.py",
        "src/core/image_generator.py",
        "src/config/settings.py",
        "src/models/content.py"
    ]
    
    # Leer contenidos de los archivos
    codigos_proyecto = {}
    for archivo in archivos_proyecto:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                codigos_proyecto[archivo] = f.read()
        except Exception as e:
            st.warning(f"Could not read {archivo}: {e}")
    
    if st.button("Generar Recursos de Desarrollo"):
        # Inicializar managers
        prompt_manager = PromptManager()
        llm_manager = LLMManager(provider=llm_provider)
        
        # Generar requirements.txt
        prompt_requirements = """Genera un archivo requirements.txt para este proyecto de aplicación Streamlit con múltiples funcionalidades. 
        Basa los requirements en los siguientes archivos de código:
        
        Archivos del proyecto:
        {archivos_codigo}
        
        Incluye todas las bibliotecas necesarias para ejecutar:
        - Streamlit
        - Generación de contenido con LLM
        - Información financiera
        - Contenido científico
        - Generación de imágenes
        
        Asegúrate de incluir las versiones específicas de cada librería.""".format(
            archivos_codigo="\n".join([f"- {arch}" for arch in codigos_proyecto.keys()])
        )
        
        requirements = llm_manager.generate_content(
            prompt_requirements, 
            "requirements", 
            "Generación de requirements.txt",
            "Desarrolladores de software"
        )
        
        # Generar README.md
        prompt_readme = """Genera un README.md completo para este proyecto de aplicación Streamlit con múltiples funcionalidades. 
        Incluye:
        - Descripción general del proyecto
        - Características principales
        - Requisitos del sistema
        - Instrucciones de instalación
        - Guía de uso
        - Estructura del proyecto
        - Tecnologías utilizadas
        
        Basa la documentación en los siguientes archivos de código:
        {archivos_codigo}
        
        Enfócate en explicar cada módulo y funcionalidad.""".format(
            archivos_codigo="\n".join([f"- {arch}" for arch in codigos_proyecto.keys()])
        )
        
        readme = llm_manager.generate_content(
            prompt_readme, 
            "readme", 
            "Generación de README.md",
            "Desarrolladores técnicos"
        )
        
        # Generar Dockerfile
        prompt_dockerfile = """Genera un Dockerfile para dockerizar esta aplicación Streamlit.
        Considera:
        - Usar una imagen base de Python
        - Instalar dependencias desde requirements.txt
        - Configurar variables de entorno
        - Exponer puerto para Streamlit
        - Copiar archivos necesarios
        - Comando de inicio para la aplicación
        
        Archivos del proyecto:
        {archivos_codigo}""".format(
            archivos_codigo="\n".join([f"- {arch}" for arch in codigos_proyecto.keys()])
        )
        
        dockerfile = llm_manager.generate_content(
            prompt_dockerfile, 
            "dockerfile", 
            "Generación de Dockerfile",
            "Equipos de DevOps"
        )
        
         
         # Crear un archivo ZIP en memoria
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr('requirements.txt', requirements.text)
            zip_file.writestr('README.md', readme.text)
            zip_file.writestr('Dockerfile', dockerfile.text)
        
        # Resetear el puntero del buffer
        zip_buffer.seek(0)
        
        # Botón de descarga único para todos los archivos
        st.download_button(
            label="📦 Descargar Todos los Recursos",
            data=zip_buffer,
            file_name="developer_resources.zip",
            mime="application/zip"
        )
        
        # Mostrar contenidos de los archivos para previsualización
        st.subheader("🔧 Recursos Generados")
        
        # Pestañas para mostrar contenidos
        tab1, tab2, tab3 = st.tabs(["requirements.txt", "README.md", "Dockerfile"])
        
        with tab1:
            st.code(requirements.text, language="txt")
        
        with tab2:
            st.code(readme.text, language="markdown")
        
        with tab3:
            st.code(dockerfile.text, language="dockerfile")       
if __name__ == "__main__":
    main()
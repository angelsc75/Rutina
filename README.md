 ![Rutina Logo](src/images/rutina_logo_baja.png)




## Descripción general del proyecto
Este proyecto está realizado dentro del bootcamp de IA de Factoría F5, que tuvo lugar entre mayo de 2024 y marzo de 2025. Es un proyecto individual que corresponde a la parte de LLM´s.

Esta aplicación es una interfaz interactiva construida con Streamlit que integra diversas funcionalidades avanzadas relacionadas con el procesamiento de lenguaje natural (NLP), generación de imágenes, y noticias financieras. Está diseñada para ayudar a los usuarios a explorar y generar contenido de manera eficiente y amigable.

## Características principales

## Resumen de Cada Módulo

Rutina se compone de varios módulos, cada uno diseñado para satisfacer diferentes necesidades de contenido. A continuación, se presenta un desglose detallado de las funcionalidades de cada uno.

### 1. Generación de Contenido para Plataformas de Redes Sociales

Este módulo permite a los usuarios generar contenido adaptado a diversas plataformas como Twitter, Instagram, LinkedIn y más. Los usuarios pueden ingresar un tema y audiencia objetivo específica, y Rutina generará automáticamente contenido optimizado para la plataforma seleccionada.

**Ejemplo de uso:**
- Un usuario que desea crear un post de Instagram sobre "La IA en el arte" puede simplemente introducir este tema y seleccionar "Instagram". Rutina generará un texto atractivo y sugerirá hashtags relevantes.

### 2. Recuperación de Información Financiera

Este módulo permite acceder a información financiera actualizada y análisis del mercado. Los usuarios pueden seleccionar un índice bursátil específico y obtener datos sobre el rendimiento del mercado, así como las acciones más destacadas.

**Ejemplo de uso:**
- Un inversor que esté interesado en el rendimiento del S&P 500 puede obtener un informe que incluya el precio actual, cambios, y la lista de las cinco acciones más destacadas del índice.

### 3. Generación de Contenido Científico

El módulo de contenido científico permite a los usuarios realizar consultas específicas sobre un área científica y recibir un informe detallado, junto con un resumen de artículos relevantes.

**Ejemplo de uso:**
- Un investigador que desee explorar el impacto del cambio climático en la biodiversidad puede introducir su consulta en Rutina y recibir un informe completo que incluya referencias a artículos académicos relevantes.

### 4. Generación de Imágenes Impulsada por IA

Los usuarios también pueden utilizar Rutina para generar imágenes relacionadas con su contenido. Este módulo permite la creación de imágenes utilizando modelos de IA como DALL-E o la búsqueda de imágenes libres de derechos en bancos de imágenes como Unsplash y Pixabay.

**Ejemplo de uso:**
- Al crear contenido para un blog sobre "La importancia de la salud mental", un usuario puede optar por generar una imagen conceptual que complemente el texto, simplemente describiendo la imagen deseada.

## Tecnologías y Frameworks Utilizados

Rutina se basa en un conjunto de tecnologías y frameworks robustos para ofrecer su amplia gama de funcionalidades:

- **Streamlit:** Para la construcción de la interfaz de usuario, facilitando la implementación de aplicaciones interactivas de ciencia de datos.
- **OpenAI y otros proveedores de LLM:** Para la generación de texto y contenido creativo mediante modelos avanzados de procesamiento de lenguaje natural.
- **YFinance:** Para la obtención de datos financieros en tiempo real.
- **ArXiv API:** Para buscar y recuperar artículos científicos de la amplia base de datos de arXiv.
- **Graphviz:** Utilizado para la visualización de grafos de relaciones en el contenido científico generado.

## Instrucciones de instalación
1. Clonar el repositorio:
   ```bash
   git clone https://github.com/tu_usuario/nombre_del_repositorio.git
   cd nombre_del_repositorio
   ```
2. Crear un entorno virtual y activarlo (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
   ```
3. Instalar las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```
4. Configurar las variables de entorno si es necesario, especialmente para servicios externos utilizados en la generación de contenido.

## Guía de uso
Para ejecutar la aplicación, simplemente utiliza el siguiente comando en el terminal:

```bash
streamlit run src/app.py
```

Esto abrirá una ventana en tu navegador predeterminado donde podrás interactuar con las diferentes funcionalidades de la aplicación.

## Estructura del proyecto
La estructura del proyecto es la siguiente:

```
nombre_del_repositorio/
│
├── src/
│   ├── app.py                         # Archivo principal de la aplicación Streamlit
│   ├── core/                           # Módulos principales del sistema
│   │   ├── llm_manager.py              # Gestión de modelos de lenguaje
│   │   ├── prompt_manager.py            # Gestión de prompts
│   │   ├── financial_news_generator.py  # Generador de noticias financieras
│   │   ├── scientific_rag.py           # Generación de contenido científico
│   │   ├── image_generator.py           # Generación de imágenes
│   │
│   ├── config/
│   │   └── settings.py                  # Configuraciones globales
│   │
│   └── models/
│       └── content.py                   # Modelo de contenido
│
└── requirements.txt                      # Dependencias del proyecto
```


## Módulos y funcionalidades

### `src/app.py`
Es el archivo principal que inicia la aplicación Streamlit. Define la interfaz de usuario y conecta todas las funcionalidades del backend.

### `src/core/llm_manager.py`
Este módulo gestiona la carga y la interacción con los modelos de lenguaje. Implementa funciones para la inferencia de textos basados en prompts. Los modelos de LLM´s son "gpt-4o-mini", de OpenAI y "llama3-8b-8192" de Groq

### `src/core/prompt_manager.py`
Ofrece herramientas para la creación, almacenamiento y manejo de prompts que se pasan a los modelos de LLM´s, optimizando así las consultas de los usuarios.

### `src/core/financial_news_generator.py`
Genera automáticamente noticias financieras utilizando datos de mercado y técnicas de NLP, permitiendo personalizar la información generada.

### `src/core/scientific_rag.py`
Implementa un sistema de Recuperación Aumentativa que ayuda a generar resúmenes y contextos sobre contenido científico, facilitando la comprensión de temas complejos.

### `src/core/image_generator.py`
Este módulo proporciona la funcionalidad para generar imágenes a partir de descripciones textuales, utilizando modelos generativos que transforman texto a visual. Los modelos son "dall-e" (de OpenAI) y "runwayml/stable-diffusion-v1-5" de StableDiffusion. También se da la opción de hacer llamadas a bancos de imágenes a través de las API de Unsplash y Pixabay.


### `src/config/settings.py`
Contiene las configuraciones y parámetros globales para la aplicación, incluyendo rutas, claves API y demás parámetros que pueden ser ser utilizados en distintos módulos.

### `src/models/content.py`
Define la estructura y el modelo de contenido que se utilizará en la aplicación, asegurando que los datos se manejen de manera consistente a través de los diferentes módulos.

### Artículo escrito en Medium por la propia aplicación
Una funcionalidad pedida en el briefing del proyecto era escribir un artículo en Medium sobre la propia aplicación. Al ser una aplicación cuya funcionalidad principal es la creación de contenido, se crea un prompt específico para la redacción de dicho artículo. El prompt se hace con el modelo de OpenAI, en español, y permite introducir el nombre de la aplicación y el título del artículo. [Link del artículo](https://medium.com/@asc7es/rutina-por-rutina-ce11613cd3c9)

### Presentación comercial de la aplicación
Otra exigencia del briefing del proyecto es una presentación comercial de la aplicación, que indique el problema al que pretende poner solución. La aplicación se crea bajo la premisa de dejar a los modelos de IA el hacer las tareas creativas que cognitivamente producen agotamiento y dejar al trabajador humano tareas más rutinarias y repetitivas que se relacionan con una buena salud mental. Las imágenes y parte del texto han sido generadas por la propia aplicación. El logo no. 
[Link a la presentación comercial](src/images/presentación_rutina.pdf)




¡Esperamos que disfrutes utilizando esta aplicación y que te sea de gran ayuda en tus tareas! Si tienes alguna pregunta, no dudes en abrir un issue en el repositorio.

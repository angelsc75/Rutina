# README.md

# Aplicación Streamlit

## Descripción general del proyecto
Esta aplicación es una interfaz interactiva construida con Streamlit que integra diversas funcionalidades avanzadas relacionadas con el procesamiento de lenguaje natural (NLP), generación de imágenes, y noticia financieras. Está diseñada para ayudar a los usuarios a explorar y generar contenido de manera eficiente y amigable.

## Características principales
- **Generación de Noticias Financieras:** Utiliza técnicas de NLP para crear noticias financieras personalizadas basadas en datos de mercado.
- **Generación de Contenido Científico:** Permite a los usuarios generar resúmenes y contextos científicos utilizando un sistema de Recuperación Aumentativa (RAG).
- **Generación de Imágenes:** Proporciona la funcionalidad para crear imágenes basadas en descripciones usando modelos generativos de IA.
- **Gestión de Prompts:** Facilita la creación y manejo de prompts (instrucciones) que se utilizan en los modelos de lenguaje para obtener respuestas más precisas.
- **Interacción en Tiempo Real:** La interfaz de usuario es completamente interactiva, permitiendo a los usuarios experimentar con diferentes entradas y ver resultados en tiempo real.

## Requisitos del sistema
- Python 3.7 o superior
- Pip (Gestor de paquetes de Python)
- Biblioteca Streamlit
- Biblioteca para la gestión de datos de NLP (como `transformers` o `spaCy`)
- Biblioteca para generación de imágenes (como `PIL` o `OpenCV`)

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

## Tecnologías utilizadas
- **Streamlit:** Para construir la interfaz de usuario interactiva.
- **Python:** Lenguaje de programación principal del proyecto.
- **Transformers:** Biblioteca para el tratamiento de modelos de lenguaje.
- **Pandas y NumPy:** Para la manipulación y análisis de datos.
- **Pillow o OpenCV:** Para el manejo y generación de imágenes.

## Módulos y funcionalidades

### `src/app.py`
Es el archivo principal que inicia la aplicación Streamlit. Define la interfaz de usuario y conecta todas las funcionalidades del backend.

### `src/core/llm_manager.py`
Este módulo gestiona la carga y la interacción con los modelos de lenguaje. Implementa funciones para la inferencia de textos basados en prompts.

### `src/core/prompt_manager.py`
Ofrece herramientas para la creación, almacenamiento y manejo de prompts que se pasan a los modelos de NLP, optimizando así las consultas de los usuarios.

### `src/core/financial_news_generator.py`
Genera automáticamente noticias financieras utilizando datos de mercado y técnicas de NLP, permitiendo personalizar la información generada.

### `src/core/scientific_rag.py`
Implementa un sistema de Recuperación Aumentativa que ayuda a generar resúmenes y contextos sobre contenido científico, facilitando la comprensión de temas complejos.

### `src/core/image_generator.py`
Este módulo proporciona la funcionalidad para generar imágenes a partir de descripciones textuales, utilizando modelos generativos que transforman texto a visual.

### `src/config/settings.py`
Contiene las configuraciones y parámetros globales para la aplicación, incluyendo rutas, claves API y demás parámetros que pueden ser ser utilizados en distintos módulos.

### `src/models/content.py`
Define la estructura y el modelo de contenido que se utilizará en la aplicación, asegurando que los datos se manejen de manera consistente a través de los diferentes módulos.

¡Esperamos que disfrutes utilizando esta aplicación y que te sea de gran ayuda en tus tareas! Si tienes alguna pregunta, no dudes en abrir un issue en el repositorio.
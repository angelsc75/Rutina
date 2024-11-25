import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuraciones existentes...
AVAILABLE_PLATFORMS = [
    "blog",
    "twitter",
    "instagram",
    "linkedin"
]

# Añadir configuración de API
API_SETTINGS = {
    "huggingface_token": os.getenv("HUGGINGFACE_API_TOKEN"),
    "model_id": "gpt2",  # Un modelo más potente que gpt2
}

# Resto de configuraciones...

# Configuración del modelo (usando Hugging Face como ejemplo)
MODEL_SETTINGS = {
    "model_id": "gpt2",  # Puedes cambiar a otro modelo gratuito de Hugging Face
    "max_length": 1000,
    "temperature": 0.3
}

# Configuración de la aplicación web
APP_SETTINGS = {
    "title": "Generador de Contenido",
    "description": "Genera contenido personalizado para diferentes plataformas"
}
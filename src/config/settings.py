import os
from dotenv import load_dotenv

load_dotenv()

AVAILABLE_PLATFORMS = [
    "blog",
    "twitter", 
    "instagram", 
    "linkedin"
]

API_SETTINGS = {
    "openai_api_key": os.getenv("OPENAI_API_KEY")
}

MODEL_SETTINGS = {
    "model": "gpt-4o-mini",  # Nuevo modelo
    "temperature": 0.7,
    "max_tokens": 1000
}

APP_SETTINGS = {
    "title": "Generador de Contenido",
    "description": "Genera contenido personalizado para diferentes plataformas"
}
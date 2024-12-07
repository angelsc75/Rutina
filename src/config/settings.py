import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDERS = {
    "openai": {
        "model": "gpt-4o-mini",
        "api_key": os.getenv("OPENAI_API_KEY")
    },
    "groq": {
        "model": "llama3-8b-8192", 
        "api_key": os.getenv("GROQ_API_KEY")
    }
}

AVAILABLE_PLATFORMS = [
    "blog",
    "twitter", 
    "instagram", 
    "linkedin"
]



MODEL_SETTINGS = {
    "model": "gpt-4o-mini", 
    "temperature": 0.7,
    "max_tokens": 1000
}

APP_SETTINGS = {
    "title": "Generador de Contenido",
    "description": "Genera contenido personalizado para diferentes plataformas"
}
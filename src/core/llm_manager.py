import traceback
from models.content import Content
import uuid
from langsmith import traceable

class LLMManager:
    def __init__(self, provider='openai'):
        self.provider = provider
        
        # Importaciones condicionales para evitar errores
        try:
            if provider == 'openai':
                from openai import OpenAI
                self.client = OpenAI()  # Sin parámetros
                self.model = "gpt-4o-mini"
            elif provider == 'groq':
                from groq import Groq
                self.client = Groq()  # Sin parámetros
                self.model = "llama3-8b-8192"
            else:
                raise ValueError(f"Proveedor no soportado: {provider}")
        
        except ImportError as e:
            print(f"Error de importación: {e}")
            raise
        except Exception as e:
            print(f"Error de inicialización: {e}")
            raise
    @traceable(name="generate_content")
    def generate_content(self, prompt, platform, topic, audience, language="castellano"):
        try:
            if not prompt:
                raise ValueError("El prompt no puede estar vacío")
            
            # Simulación si no hay cliente real
            if not hasattr(self, 'client'):
                return Content(
                    id=str(uuid.uuid4()),
                    platform=platform,
                    topic=topic,
                    audience=audience,
                    language=language,
                    text=f"Contenido simulado para {topic}"
                )
            extra_metadata = {
            "platform": platform,
            "tema": topic,
            "audiencia": audience
        }
            # Generación de contenido
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system", 
                        "content": f"You are an expert content generation assistant. Respond in {language}."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ]
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            return Content(
                id=str(uuid.uuid4()),
                platform=platform,
                topic=topic,
                audience=audience,
                language=language,
                text=generated_text
            )
            
        except Exception as e:
            error_details = f"Error en generación de contenido: {str(e)}\n{traceback.format_exc()}"
            print(error_details)
            raise RuntimeError(error_details)
from openai import OpenAI
from config.settings import API_SETTINGS, MODEL_SETTINGS
from models.content import Content
import uuid

class LLMManager:
    def __init__(self):
        self.client = OpenAI(api_key=API_SETTINGS["openai_api_key"])
    
    def generate_content(self, prompt, platform, topic, audience) -> Content:
        try:
            response = self.client.chat.completions.create(
                model=MODEL_SETTINGS["model"],
                messages=[
                    {"role": "system", "content": "Eres un asistente experto en generación de contenido para redes sociales."},
                    {"role": "user", "content": prompt}
                ],
                temperature=MODEL_SETTINGS["temperature"],
                max_tokens=MODEL_SETTINGS["max_tokens"]
            )
            
            generated_text = response.choices[0].message.content.strip()
            
            # Crear objeto Content
            content = Content(
                id=str(uuid.uuid4()),  # Genera un ID único
                platform=platform,
                topic=topic,
                audience=audience,
                text=generated_text
            )
            
            return content
        
        except Exception as e:
            print(f"Error generando contenido: {e}")
            return None
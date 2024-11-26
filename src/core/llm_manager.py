from openai import OpenAI
from config.settings import MODEL_SETTINGS, LLM_PROVIDERS
from models.content import Content
import uuid

from groq import Groq

class LLMManager:
    def __init__(self, provider='openai'):
        self.provider = provider
        
        if provider == 'openai':
            self.client = OpenAI(api_key=LLM_PROVIDERS['openai']['api_key'])
            self.model = LLM_PROVIDERS['openai']['model']
        elif provider == 'groq':
            self.client = Groq(api_key=LLM_PROVIDERS['groq']['api_key'])
            self.model = LLM_PROVIDERS['groq']['model']
    
    def generate_content(self, prompt, platform, topic, audience):
        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un asistente experto en generación de contenido."},
                        {"role": "user", "content": prompt}
                    ]
                )
                generated_text = response.choices[0].message.content.strip()
            
            elif self.provider == 'groq':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un asistente experto en generación de contenido."},
                        {"role": "user", "content": prompt}
                    ]
                )
                generated_text = response.choices[0].message.content.strip()
            
            content = Content(
                id=str(uuid.uuid4()),
                platform=platform,
                topic=topic,
                audience=audience,
                text=generated_text
            )
            
            return content
        
        except Exception as e:
            print(f"Error generando contenido: {e}")
            return None
from openai import OpenAI
from config.settings import MODEL_SETTINGS, LLM_PROVIDERS
from models.content import Content
import uuid
from langsmith import traceable
from groq import Groq

class LLMManager:
    def __init__(self, provider='openai'):
        # Importación opcional de LangSmith
        try:
            from langsmith import Client
            self.langsmith_client = Client()
            self.use_langsmith = True
        except ImportError:
            self.langsmith_client = None
            self.use_langsmith = False
        
        self.provider = provider
        
        if provider == 'openai':
            self.client = OpenAI(api_key=LLM_PROVIDERS['openai']['api_key'])
            self.model = LLM_PROVIDERS['openai']['model']
        elif provider == 'groq':
            self.client = Groq(api_key=LLM_PROVIDERS['groq']['api_key'])
            self.model = LLM_PROVIDERS['groq']['model']
    
    @traceable  # Decorador de LangSmith para trazabilidad
    def generate_content(self, prompt, platform, topic, audience, language="castellano"):
        try:
            if self.provider == 'openai':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are an expert content generation assistant. Respond in {language}."},
                        {"role": "user", "content": prompt}
                    ]
                )
                generated_text = response.choices[0].message.content.strip()
            
            elif self.provider == 'groq':
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": f"You are an expert content generation assistant. Respond in {language}."},
                        {"role": "user", "content": prompt}
                    ]
                )
                generated_text = response.choices[0].message.content.strip()
            
            content = Content(
                id=str(uuid.uuid4()),
                platform=platform,
                topic=topic,
                audience=audience,
                language=language,  # Add language to the Content model
                text=generated_text
            )
            
            return content
        
        except Exception as e:
            # Loguear el error si es necesario
            print(f"Error en generación de contenido: {e}")
            raise
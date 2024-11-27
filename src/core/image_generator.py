from openai import OpenAI
import os

class ImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    def generate_image(self, prompt, platform):
        try:
            # Dimensiones específicas para cada plataforma
            platform_sizes = {
                "blog": "1024x1024",
                "twitter": "1024x1024", 
                "instagram": "1024x1024",
                "linkedin": "1024x1024"
            }
            
            # Genera la imagen con DALL-E 3
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size=platform_sizes.get(platform, "1024x1024"),
                quality="standard",
                n=1
            )
            
            # Obtiene la URL de la imagen generada
            image_url = response.data[0].url
            
            # Descarga la imagen
            import requests
            image_response = requests.get(image_url)
            return image_response.content
        
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return None
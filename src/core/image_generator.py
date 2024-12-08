import os
import logging
import torch
import io
import requests
from PIL import Image
from diffusers import StableDiffusionPipeline
from openai import OpenAI
from dotenv import load_dotenv
from langsmith import Client, traceable


# Cargar variables de entorno
load_dotenv()

class ImageGenerator:
    # Definir dimensiones específicas para cada plataforma
    PLATFORM_SIZES = {
        'blog': (1200, 632),      # Ajustado para ser divisible por 8
        'instagram': (1080, 1080), # Ya es divisible por 8
        'linkedin': (1200, 632),   # Ajustado para ser divisible por 8
        'twitter': (1200, 672)     # Ajustado para ser divisible por 8
    }

    def __init__(self, huggingface_token=None):
        # Configurar logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Añadir un handler de consola si no existe
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)
        # Configurar LangSmith
        try:
            self.langsmith_client = Client(
                api_key=os.getenv('LANGCHAIN_API_KEY'),
                
            )
        except Exception as e:
            self.logger.error(f"Error inicializando LangSmith: {e}")
            self.langsmith_client = None
            
        

        # Inicializar clientes para servicios
        try:
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            self.logger.error(f"Error inicializando cliente OpenAI: {e}")
            self.openai_client = None
        
        # Obtener API key de Unsplash desde variables de entorno
        self.unsplash_access_key = os.getenv("UNSPLASH_ACCESS_KEY")
        
        # Inicializar Stable Diffusion
        try:
            # Cargar modelo Stable Diffusion
            self.sd_model = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5", 
                torch_dtype=torch.float32,
                safety_checker=None
            )
            
            # Mover explícitamente a CPU
            self.sd_model = self.sd_model.to("cpu")
            
            self.logger.info("Stable Diffusion model loaded successfully")
        
        except Exception as e:
            self.logger.error(f"Error cargando modelo Stable Diffusion: {e}")
            import traceback
            traceback.print_exc()
            self.sd_model = None

    def _validate_and_adjust_size(self, width, height):
        """
        Ajusta las dimensiones para que sean divisibles por 8
        """
        def round_to_8(n):
            return int(round(n / 8) * 8)
        
        adjusted_width = round_to_8(width)
        adjusted_height = round_to_8(height)
        
        if width != adjusted_width or height != adjusted_height:
            self.logger.warning(f"Ajustando tamaño de {width}x{height} a {adjusted_width}x{adjusted_height}")
        
        return adjusted_width, adjusted_height

    @traceable(name="get_unsplash_image")
    def _get_unsplash_image(self, prompt, width, height):
        """
        Obtener imagen desde Unsplash
        """
        if not self.unsplash_access_key:
            self.logger.error("Unsplash access key no configurada")
            return None
        
        try:
            # Parámetros para buscar imagen
            params = {
                'query': prompt,
                'client_id': self.unsplash_access_key,
                'w': width,
                'h': height,
                'fit': 'crop'  # Recortar para ajustar dimensiones exactas
            }
            
            # Realizar solicitud a API de Unsplash
            response = requests.get(
                "https://api.unsplash.com/photos/random", 
                params=params
            )
            
            # Verificar respuesta
            if response.status_code == 200:
                data = response.json()
                image_url = data['urls']['custom']  # URL de imagen con dimensiones personalizadas
                
                # Descargar imagen
                image_response = requests.get(image_url)
                if image_response.status_code == 200:
                    return image_response.content
            
            self.logger.error(f"Error obteniendo imagen de Unsplash: {response.status_code}")
            return None
        
        except Exception as e:
            self.logger.error(f"Error en búsqueda de Unsplash: {e}")
            return None
    @traceable(name="generate_image")
    def generate_image(self, prompt, platform, generator='unsplash'):
        try:
            # Obtener tamaño específico de plataforma, con fallback a un tamaño genérico
            size = self.PLATFORM_SIZES.get(platform, (1024, 1024))
            width, height = size

            # Seleccionar generador de imagen
            if generator == 'unsplash':
                return self._get_unsplash_image(prompt, width, height)
            
            elif generator == 'stable-diffusion':
                # Verificar si el modelo está inicializado
                if self.sd_model is None:
                    self.logger.error("Stable Diffusion model is not initialized")
                    return None

                try:
                    # Generar imagen con Stable Diffusion
                    images = self.sd_model(
                        prompt=prompt, 
                        num_inference_steps=20,
                        guidance_scale=7.5,
                        width=width,   # Usar ancho original
                        height=height  # Usar alto original
                    ).images
                    
                    if not images:
                        self.logger.error("No images were generated")
                        return None
                    
                    # Redimensionar imagen al tamaño exacto 
                    resized_image = images[0].resize((width, height), Image.LANCZOS)
                    
                    # Convertir a bytes
                    img_byte_arr = io.BytesIO()
                    resized_image.save(img_byte_arr, format='PNG')
                    return img_byte_arr.getvalue()
                
                except Exception as sd_err:
                    self.logger.error(f"Detailed Stable Diffusion error: {sd_err}")
                    import traceback
                    traceback.print_exc()
                    return None
            
            elif generator == 'dall-e':
                # Verificar si OpenAI client está inicializado
                if self.openai_client is None:
                    self.logger.error("OpenAI client is not initialized")
                    return None

                try:
                    # Mapear tamaños personalizados a tamaños estándar de DALL-E
                    dall_e_sizes = ['256x256', '512x512', '1024x1024', '1024x1792', '1792x1024']
                    
                    # Función para encontrar el tamaño estándar más cercano
                    def find_closest_size(width, height):
                        # Si ya es un tamaño estándar, úsalo
                        if f"{width}x{height}" in dall_e_sizes:
                            return f"{width}x{height}"
                        
                        # Mapeo de tamaños específicos a los más cercanos de DALL-E
                        size_mapping = {
                            (1200, 632): '1792x1024',   # Blog/LinkedIn
                            (1080, 1080): '1024x1024',  # Instagram
                            (1200, 672): '1792x1024'    # Twitter
                        }
                        
                        # Buscar mapeo directo primero
                        if (width, height) in size_mapping:
                            return size_mapping[(width, height)]
                        
                        # Si no hay mapeo directo, elegir el tamaño más cercano
                        return '1024x1024'  # Fallback al tamaño estándar más común
                    
                    # Encontrar el tamaño más apropiado
                    size_str = find_closest_size(width, height)
                    
                    self.logger.info(f"Usando tamaño DALL-E: {size_str} (original solicitado: {width}x{height})")
                    
                    # Generar imagen
                    response = self.openai_client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size=size_str
                    )
                    return response.data[0].url
                except Exception as e:
                    self.logger.error(f"DALL-E image generation error: {e}")
                    return None
            
            else:
                self.logger.error(f"Invalid image generator: {generator}")
                raise ValueError("Generador de imágenes no válido")
        
        except Exception as e:
            self.logger.error(f"Error generando imagen: {e}")
            return None
import os
import logging
import torch
import io
from PIL import Image
from diffusers import StableDiffusionPipeline
from openai import OpenAI

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

        # Inicializar clientes para ambos servicios
        try:
            self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        except Exception as e:
            self.logger.error(f"Error inicializando cliente OpenAI: {e}")
            self.openai_client = None
        
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

    def generate_image(self, prompt, platform, generator='dall-e'):
        try:
            # Obtener tamaño específico de plataforma, con fallback a un tamaño genérico
            size = self.PLATFORM_SIZES.get(platform, (1024, 1024))

            if generator == 'stable-diffusion':
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
                        width=size[0],   # Usar ancho específico
                        height=size[1]   # Usar alto específico
                    ).images
                    
                    if not images:
                        self.logger.error("No images were generated")
                        return None
                    
                    # Redimensionar imagen al tamaño exacto de la plataforma
                    resized_image = images[0].resize(size, Image.LANCZOS)
                    
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
                    # Implementar lógica para DALL-E
                    response = self.openai_client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size=f"{size[0]}x{size[1]}"
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
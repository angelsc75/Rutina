import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import os
from stability_sdk import client  # Change this import
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
class ImageGenerator:
    def __init__(self):
        self.client = client.StabilityInference(os.getenv("STABILITY_API_KEY"))
    
    def generate_image(self, prompt, platform):
        try:
            # Definir dimensiones según la plataforma
            platform_dimensions = {
                "blog": {"width": 1200, "height": 630},      # Tamaño óptimo para blogs y contenido web
                "twitter": {"width": 1200, "height": 675},   # Relación 16:9 para Twitter
                "instagram": {"width": 1080, "height": 1080}, # Cuadrado para Instagram
                "linkedin": {"width": 1200, "height": 628}   # Dimensiones recomendadas para LinkedIn
            }
            
            # Obtener dimensiones, por defecto 1024x1024 si la plataforma no está definida
            dimensions = platform_dimensions.get(platform, {"width": 1024, "height": 1024})
            
            answers = self.client.generate(
                prompt=prompt,
                width=dimensions["width"],
                height=dimensions["height"]
            )
            
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        return artifact.binary  # Devuelve la imagen
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return None  
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import os

class ImageGenerator:
    def __init__(self):
        self.client = Client(os.getenv("STABILITY_API_KEY"))
    
    def generate_image(self, prompt):
        try:
            answers = self.client.generate(
                prompt=prompt,
                width=1024,
                height=1024
            )
            
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.type == generation.ARTIFACT_IMAGE:
                        return artifact.binary  # Devuelve la imagen
        except Exception as e:
            print(f"Error generando imagen: {e}")
            return None  
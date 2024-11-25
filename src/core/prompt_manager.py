class PromptManager:
    def __init__(self):
        self.templates = {
            "blog": """Escribe un artículo de blog sobre {tema}.
                      Audiencia objetivo: {audiencia}
                      Tono: {tono}
                      Longitud aproximada: 500 palabras""",
            
            "twitter": """Crea un tweet conciso y atractivo sobre {tema}.
                         Audiencia: {audiencia}
                         Debe ser menor a 280 caracteres.""",
            
            "instagram": """Genera una descripción atractiva para Instagram sobre {tema}.
                          Incluye hashtags relevantes.
                          Audiencia: {audiencia}""",
            
            "linkedin": """Crea una publicación profesional para LinkedIn sobre {tema}.
                          Enfocado a: {audiencia}
                          Tono: profesional y constructivo"""
        }
    
    def get_prompt(self, platform, tema, audiencia, tono="neutral"):
        template = self.templates.get(platform)
        return template.format(tema=tema, audiencia=audiencia, tono=tono)
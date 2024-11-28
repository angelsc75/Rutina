class PromptManager:
    def __init__(self):
        self.templates = {
            "castellano": {
                "blog": """Escribe una entrada de blog completa sobre {topic}.
                          Audiencia objetivo: {audience}
                          Tono: {tone}
                          Longitud aproximada: 500 palabras
                          Enfócate en proporcionar ideas prácticas y contenido atractivo.""",
                
                "twitter": """Crea un tweet conciso e impactante sobre {topic}.
                             Audiencia objetivo: {audience}
                             Debe tener menos de 280 caracteres
                             Incluye un gancho o idea clave convincente.""",
                
                "instagram": """Crea un pie de foto de Instagram atractivo para {topic}.
                              Incluye hashtags relevantes y de tendencia
                              Audiencia objetivo: {audience}
                              Hazlo visualmente atractivo y compartible""",
                
                "linkedin": """Desarrolla una publicación profesional de LinkedIn sobre {topic}.
                              Dirigida a: {audience}
                              Tono: profesional, autoritario y generador de valor
                              Destaca ideas profesionales o tendencias de la industria"""
            },
            "english": {
                "blog": """Write a comprehensive blog post about {topic}.
                          Target audience: {audience}
                          Tone: {tone}
                          Approximate length: 500 words
                          Focus on providing actionable insights and engaging content.""",
                
                "twitter": """Craft a concise, impactful tweet about {topic}.
                             Target audience: {audience}
                             Must be under 280 characters
                             Include a compelling hook or key takeaway.""",
                
                "instagram": """Create an engaging Instagram caption for {topic}.
                              Include relevant and trending hashtags
                              Target audience: {audience}
                              Make it visually appealing and shareable""",
                
                "linkedin": """Develop a professional LinkedIn post about {topic}.
                              Targeted to: {audience}
                              Tone: professional, authoritative, and value-driven
                              Highlight key professional insights or industry trends"""
            },
            "français": {
                "blog": """Rédigez un article de blog complet sur {topic}.
                          Public cible : {audience}
                          Ton : {tone}
                          Longueur approximative : 500 mots
                          Concentrez-vous sur la fourniture d'idées pratiques et de contenu attrayant.""",
                
                "twitter": """Créez un tweet concis et percutant sur {topic}.
                             Public cible : {audience}
                             Doit tenir en moins de 280 caractères
                             Incluez un crochet ou un point clé convaincant.""",
                
                "instagram": """Créez une légende Instagram attrayante pour {topic}.
                              Incluez des hashtags pertinents et tendance
                              Public cible : {audience}
                              Rendez-le visuellement attrayant et partageable""",
                
                "linkedin": """Développez un post LinkedIn professionnel sur {topic}.
                              Destiné à : {audience}
                              Ton : professionnel, autoritaire et axé sur la valeur
                              Mettez en avant des perspectives professionnelles ou des tendances de l'industrie"""
            },
            "italiano": {
                "blog": """Scrivi un post di blog completo su {topic}.
                          Pubblico target: {audience}
                          Tono: {tone}
                          Lunghezza approssimativa: 500 parole
                          Concentrati sul fornire spunti pratici e contenuti coinvolgenti.""",
                
                "twitter": """Crea un tweet conciso e di impatto su {topic}.
                             Pubblico target: {audience}
                             Deve essere inferiore a 280 caratteri
                             Includi un gancio o un punto chiave convincente.""",
                
                "instagram": """Crea una didascalia Instagram coinvolgente per {topic}.
                              Includi hashtag rilevanti e di tendenza
                              Pubblico target: {audience}
                              Rendilo visivamente accattivante e condivisibile""",
                
                "linkedin": """Sviluppa un post LinkedIn professionale su {topic}.
                              Destinato a: {audience}
                              Tono: professionale, autorevole e orientato al valore
                              Evidenzia intuizioni professionali o tendenze del settore"""
            }
        }
    
    def get_prompt(self, platform, tema, audiencia, idioma="castellano", tono="neutral"):
        template = self.templates.get(idioma, {}).get(platform)
        return template.format(topic=tema, audience=audiencia, tone=tono)
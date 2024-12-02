class PromptManager:
    def __init__(self):
        # All templates are now in English
        self.templates = {
            "castellano": {
                "blog": """Write a comprehensive blog post about {topic}.
                          Target audience: {audience}
                          Tone: {tone}
                          Approximate length: 500 words
                          Focus on providing actionable insights and engaging content.
                          
                          Note: Respond in Spanish (castellano).""",
                
                "twitter": """Craft a concise, impactful tweet about {topic}.
                             Target audience: {audience}
                             Must be under 280 characters
                             Include a compelling hook or key takeaway.
                             
                             Note: Respond in Spanish (castellano).""",
                
                "instagram": """Create an engaging Instagram caption for {topic}.
                              Include relevant and trending hashtags
                              Target audience: {audience}
                              Make it visually appealing and shareable.
                              
                              Note: Respond in Spanish (castellano).""",
                
                "linkedin": """Develop a professional LinkedIn post about {topic}.
                              Targeted to: {audience}
                              Tone: professional, authoritative, and value-driven
                              Highlight key professional insights or industry trends.
                              
                              Note: Respond in Spanish (castellano)."""
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
                              Make it visually appealing and shareable.""",
                
                "linkedin": """Develop a professional LinkedIn post about {topic}.
                              Targeted to: {audience}
                              Tone: professional, authoritative, and value-driven
                              Highlight key professional insights or industry trends."""
            },
            "français": {
                "blog": """Write a comprehensive blog post about {topic}.
                          Target audience: {audience}
                          Tone: {tone}
                          Approximate length: 500 words
                          Focus on providing actionable insights and engaging content.
                          
                          Note: Respond in French (français).""",
                
                "twitter": """Craft a concise, impactful tweet about {topic}.
                             Target audience: {audience}
                             Must be under 280 characters
                             Include a compelling hook or key takeaway.
                             
                             Note: Respond in French (français).""",
                
                "instagram": """Create an engaging Instagram caption for {topic}.
                              Include relevant and trending hashtags
                              Target audience: {audience}
                              Make it visually appealing and shareable.
                              
                              Note: Respond in French (français).""",
                
                "linkedin": """Develop a professional LinkedIn post about {topic}.
                              Targeted to: {audience}
                              Tone: professional, authoritative, and value-driven
                              Highlight key professional insights or industry trends.
                              
                              Note: Respond in French (français)."""
            },
            "italiano": {
                "blog": """Write a comprehensive blog post about {topic}.
                          Target audience: {audience}
                          Tone: {tone}
                          Approximate length: 500 words
                          Focus on providing actionable insights and engaging content.
                          
                          Note: Respond in Italian (italiano).""",
                
                "twitter": """Craft a concise, impactful tweet about {topic}.
                             Target audience: {audience}
                             Must be under 280 characters
                             Include a compelling hook or key takeaway.
                             
                             Note: Respond in Italian (italiano).""",
                
                "instagram": """Create an engaging Instagram caption for {topic}.
                              Include relevant and trending hashtags
                              Target audience: {audience}
                              Make it visually appealing and shareable.
                              
                              Note: Respond in Italian (italiano).""",
                
                "linkedin": """Develop a professional LinkedIn post about {topic}.
                              Targeted to: {audience}
                              Tone: professional, authoritative, and value-driven
                              Highlight key professional insights or industry trends.
                              
                              Note: Respond in Italian (italiano)."""
            }
        }
    
    def get_prompt(self, platform, tema, audiencia, idioma="castellano", tono="neutral"):
        template = self.templates.get(idioma, {}).get(platform)
        return template.format(topic=tema, audience=audiencia, tone=tono)
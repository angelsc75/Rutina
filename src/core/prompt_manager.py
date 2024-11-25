class PromptManager:
    def __init__(self):
        self.templates = {
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
        }
    
    def get_prompt(self, platform, tema, audiencia, tono="neutral"):
        template = self.templates.get(platform)
        return template.format(topic=tema, audience=audiencia, tone=tono)
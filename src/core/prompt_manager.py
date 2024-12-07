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
                              
                              Note: Respond in Spanish (castellano).""",
                "medium":    """Write a comprehensive Medium article about {app_name}, an innovative content generation application.

            Detailed description of the application, its features, and functionalities.
            Length: Approximately 2000 words
            Target Audience: Developers, tech entrepreneurs, and AI enthusiasts
            Tone: Technical yet accessible

            Sections to cover:
            1. Introduction to {app_name}
            Psychological and Productivity Perspective:
            - Explore how creative tasks generate cognitive stress
            - Analyze the mental toll of repetitive content creation
            - Position AI as a supportive tool for mental well-being
            2. Overview of each module:
            - Content generation for social media platforms
            - Financial information retrieval
            - Scientific content generation
            - AI-powered image generation
            3. Technologies and frameworks used
            4. Key benefits and use cases
            5. Future perspectives and potential improvements

            Key points to highlight:
            - Flexibility of the application
            - Multi-language support
            - Integration of different AI models
            - Unique selling points of {app_name}

            Include examples of how each functionality can be utilized.
            Showcase the versatility of the application for different user needs.

            IMPORTANT: Attach the main project files' code at the end of the article for technical context.

            Note: Respond in Spanish."""
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
            },
           
        }
    
    def get_prompt(self, platform, tema, audiencia, idioma="castellano", tono="neutral", article_title=None, app_name=None):
        template = self.templates.get(idioma, {}).get(platform)
        if article_title and app_name:
            return template.format(topic=tema, audience=audiencia, tone=tono, article_title=article_title, app_name=app_name)
        return template.format(topic=tema, audience=audiencia, tone=tono)
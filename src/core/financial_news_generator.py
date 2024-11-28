import requests
import os
from models.content import Content, ContentManager

class FinancialNewsGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
    
    def get_market_news(self, category="technology"):
        params = {
            "function": "NEWS_SENTIMENT",
            "topics": category,
            "apikey": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        return response.json()
    
    def generate_financial_content(self, news_data, language="english"):
        """
        Generate financial content based on news data and language
        
        Args:
            news_data (dict): News data from Alpha Vantage API
            language (str, optional): Language for content generation. Defaults to "english".
        
        Returns:
            Content object with generated text
        """
        # Basic error handling for news data
        if not news_data or 'feed' not in news_data:
            return Content(
                text="No financial news data available.", 
                language=language,
                topic="financial_news"
            )
        
        # Extract relevant news information
        news_items = news_data.get('feed', [])[:5]  # Limit to first 5 news items
        
        # Prepare content template
        news_summary = f"Financial Market News Report ({language.capitalize()}):\n\n"
        
        for idx, news in enumerate(news_items, 1):
            news_summary += f"{idx}. {news.get('title', 'Untitled')}\n"
            news_summary += f"   Source: {news.get('source', 'Unknown')}\n"
            news_summary += f"   Summary: {news.get('summary', 'No summary available')}\n\n"
        
        # Create and return Content object
        return Content(
            text=news_summary, 
            language=language,
            topic="financial_news",
            platform="financial_report"
        )
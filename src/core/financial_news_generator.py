import requests

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
    
    def generate_financial_content(self, news_data):
        # Procesar y sintetizar noticias
        pass
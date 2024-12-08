from dotenv import load_dotenv
import yfinance as yf
import requests
import os
from deep_translator import GoogleTranslator
from langsmith import traceable

from dotenv import load_dotenv
import yfinance as yf
import requests
import os
from deep_translator import GoogleTranslator
from langsmith import traceable

class FinancialNewsGenerator:
    def __init__(self):
        load_dotenv()
        self.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_KEY")
        if not self.alpha_vantage_api_key:
            raise ValueError("La clave de Alpha Vantage (ALPHA_VANTAGE_KEY) no está definida en el archivo .env.")
    
    @traceable(name="get_top_stocks_from_yahoo")
    def get_top_stocks_from_yahoo(self, etf_ticker, top_n=5):
        try:
            market_components = {
                "^DJI": ["AAPL", "AMGN", "AXP", "BA", "CAT", "CRM", "CSCO", 
                        "CVX", "DIS", "DOW", "GS", "HD", "HON", "IBM", 
                        "INTC", "JNJ", "JPM", "KO", "MCD", "MMM", "MRK", 
                        "MSFT", "NKE", "PG", "TRV", "UNH", "V", "VZ", "WBA", "WMT"],
                "^GSPC": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "GOOG", "UNH", "XOM"],
                "^IXIC": ["AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "META", "TSLA", "INTC", "CSCO", "AMD"],
                "^FTSE": ["SHEL", "HSBA", "LSEG", "AZN", "BP", "GSK", "ULVR", "RIO", "REL", "DGE"],
                "^N225": ["7203.T", "9984.T", "7267.T", "9433.T", "6758.T"]
            }

            components = market_components.get(etf_ticker, [])
            top_stocks = []

            for stock_symbol in components:
                stock = yf.Ticker(stock_symbol)
                hist = stock.history(period="1d")
                if not hist.empty:
                    stock_info = {
                        "symbol": stock_symbol,
                        "name": stock.info.get('longName', stock_symbol),
                        "price": hist['Close'].iloc[-1],
                        "change": hist['Close'].iloc[-1] - hist['Open'].iloc[0],
                        "change_percent": ((hist['Close'].iloc[-1] / hist['Open'].iloc[0]) - 1) * 100
                    }
                    top_stocks.append(stock_info)

            filtered_stocks = [
                stock for stock in top_stocks 
                if abs(stock['change_percent']) < 20
            ]

            filtered_stocks.sort(key=lambda x: abs(x['change_percent']), reverse=True)
            return filtered_stocks[:top_n]
        except Exception as e:
            print(f"Error fetching data from Yahoo Finance: {e}")
            return []

    @traceable(name="get_top_stocks_from_alpha")
    def get_top_stocks_from_alpha(self, market_sector=None, top_n=5):
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "TOP_GAINERS_LOSERS",
                "apikey": self.alpha_vantage_api_key
            }
            response = requests.get(url, params=params)
            data = response.json()

            if "top_gainers" in data:
                top_stocks = [
                    {
                        "symbol": stock["ticker"],
                        "name": stock["ticker"],
                        "price": float(stock["price"]),
                        "change": float(stock["change_amount"]),
                        "change_percent": float(stock["change_percentage"].strip('%'))
                    } 
                    for stock in data["top_gainers"][:top_n]
                ]
                return top_stocks
            else:
                print("Unexpected Alpha Vantage response structure")
                return []
        except Exception as e:
            print(f"Error fetching data from Alpha Vantage: {e}")
            return []

    @traceable(name="get_top_stocks_from_market")
    def get_top_stocks_from_market(self, market_ticker, top_n=5):
        etf_map = {
            "^GSPC": "SPY",
            "^IXIC": "QQQ",
            "^DJI": "DIA",
            "^FTSE": "VUKE",
            "^N225": "HJPX"
        }
        etf_ticker = etf_map.get(market_ticker, market_ticker)

        yahoo_stocks = self.get_top_stocks_from_yahoo(etf_ticker, top_n)
        if yahoo_stocks:
            return yahoo_stocks

        try:
            alpha_stocks = self.get_top_stocks_from_alpha()
            if alpha_stocks:
                return alpha_stocks
        except Exception as e:
            print(f"Alpha Vantage fallback failed: {e}")

        return []

    @traceable(name="get_market_performance")
    def get_market_performance(self, market_ticker):
        try:
            market = yf.Ticker(market_ticker)
            historical_data = market.history(period="1d")
            
            if historical_data.empty:
                return None
            
            open_price = historical_data['Open'].iloc[0]
            close_price = historical_data['Close'].iloc[-1]
            change = close_price - open_price
            change_percent = (change / open_price) * 100
            
            return {
                "current_price": close_price,
                "change": change,
                "change_percent": change_percent
            }
        except Exception as e:
            print(f"Error fetching market performance: {e}")
            return None

    @traceable(name="generate_market_report")
    def generate_market_report(self, market_ticker, top_n=5):
        top_stocks = self.get_top_stocks_from_market(market_ticker, top_n)
        market_performance = self.get_market_performance(market_ticker)
        
        report = f"Market: {market_ticker}\n"
        
        if market_performance:
            report += (
                f"Market Performance:\n"
                f"  Current Price: ${market_performance['current_price']:.2f}\n"
                f"  Change: ${market_performance['change']:.2f} "
                f"({market_performance['change_percent']:.2f}%)\n\n"
            )
        
        report += f"Top {top_n} Stocks:\n"
        for stock in top_stocks:
            report += (
                f"  {stock['name']} ({stock['symbol']}):\n"
                f"    Price: ${stock['price']:.2f}\n"
                f"    Change: ${stock['change']:.2f} ({stock['change_percent']:.2f}%)\n"
            )
        
        return report

    @traceable(name="get_financial_news")
    def get_financial_news(self, market_name, language="english"):
        load_dotenv()
        news_api_key = os.getenv("NEWSAPI_KEY")
        
        if not news_api_key:
            raise ValueError("NewsAPI key (NEWSAPI_KEY) is not defined in .env file")
        
        market_keywords = {
            "S&P 500": ["S&P 500", "stock market", "wall street", "US stocks"],
            "NASDAQ Composite": ["NASDAQ", "tech stocks", "technology market", "silicon valley"],
            "Dow Jones": ["Dow Jones", "industrial stocks", "US market"],
            "FTSE 100": ["FTSE 100", "UK stock market", "London stock exchange"],
            "Nikkei 225": ["Nikkei 225", "Japanese stock market", "Tokyo stocks"]
        }
        
        keywords = market_keywords.get(market_name, ["stock market"])
        
        for keyword in keywords:
            url = "https://newsapi.org/v2/everything"
            params = {
                "apiKey": news_api_key,
                "q": keyword,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": 5
            }
            
            try:
                response = requests.get(url, params=params)
                data = response.json()
                
                if data.get("status") == "ok" and data.get("totalResults", 0) > 0:
                    news_articles = []
                    for article in data.get("articles", [])[:3]:
                        if article.get("title") and article.get("description"):
                            news_articles.append({
                                "title": article.get("title", ""),
                                "description": article.get("description", ""),
                                "url": article.get("url", ""),
                                "source": article.get("source", {}).get("name", ""),
                                "publishedAt": article.get("publishedAt", "")
                            })
                    
                    if news_articles:
                        translated_articles = self.translate_news_articles(news_articles, language)
                        return translated_articles
            
            except Exception as e:
                print(f"Error fetching news for {keyword}: {e}")
        
        return []

    @traceable(name="translate_news_articles")
    def translate_news_articles(self, articles, target_language):
        language_map = {
            "castellano": "es",
            "english": "en",
            "français": "fr",
            "italiano": "it"
        }
        
        target_lang_code = language_map.get(target_language, "en")
        
        if target_lang_code != "en":
            translated_articles = []
            
            for article in articles:
                try:
                    translated_title = GoogleTranslator(source='auto', target=target_lang_code).translate(article['title'])
                    translated_description = GoogleTranslator(source='auto', target=target_lang_code).translate(article['description'])
                    
                    translated_articles.append({
                        "title": translated_title,
                        "description": translated_description,
                        "url": article['url'],
                        "source": article['source']
                    })
                except Exception as e:
                    print(f"Translation error: {e}")
                    translated_articles.append(article)
            
            return translated_articles
        
        return articles
from dotenv import load_dotenv
import yfinance as yf
import requests
import os


class FinancialNewsGenerator:
    def __init__(self):
        
        load_dotenv()
        self.alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_KEY")
        if not self.alpha_vantage_api_key:
            raise ValueError("La clave de Alpha Vantage (ALPHA_VANTAGE_KEY) no está definida en el archivo .env.")
    
    
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

            # Filter out stocks with extreme changes
            filtered_stocks = [
                stock for stock in top_stocks 
                if abs(stock['change_percent']) < 20  # Limit to ±20% change
            ]

            filtered_stocks.sort(key=lambda x: abs(x['change_percent']), reverse=True)
            return filtered_stocks[:top_n]
        except Exception as e:
            print(f"Error fetching data from Yahoo Finance: {e}")
            return []

    def get_top_stocks_from_alpha(self, market_sector=None, top_n=5):
        try:
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": "TOP_GAINERS_LOSERS",
                "apikey": self.alpha_vantage_api_key
            }
            response = requests.get(url, params=params)
            data = response.json()

            # Check the structure of the response
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

    def get_top_stocks_from_market(self, market_ticker, top_n=5):
        """
        Fetch top stocks for a given market index using multiple data sources.
        """
        etf_map = {
            "^GSPC": "SPY",   # S&P 500
            "^IXIC": "QQQ",   # NASDAQ
            "^DJI": "DIA",    # Dow Jones
            "^FTSE": "VUKE",  # FTSE 100
            "^N225": "HJPX"   # Nikkei 225
        }
        etf_ticker = etf_map.get(market_ticker, market_ticker)

        # Try Yahoo Finance first
        yahoo_stocks = self.get_top_stocks_from_yahoo(etf_ticker, top_n)
        if yahoo_stocks:
            return yahoo_stocks

        # Fallback to Alpha Vantage
        try:
            alpha_stocks = self.get_top_stocks_from_alpha()
            if alpha_stocks:
                return alpha_stocks
        except Exception as e:
            print(f"Alpha Vantage fallback failed: {e}")

        return []
    def get_market_performance(self, market_ticker):
        """
        Fetch overall market performance for a given index.
        """
        try:
            market = yf.Ticker(market_ticker)
            historical_data = market.history(period="1d")
            
            if historical_data.empty:
                return None
            
            # Calculate market performance metrics
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
    def generate_market_report(self, market_ticker, top_n=5):
        """
        Generate a comprehensive market report.
        """
        # Fetch top stocks
        top_stocks = self.get_top_stocks_from_market(market_ticker, top_n)
        
        # Fetch market performance
        market_performance = self.get_market_performance(market_ticker)
        
        # Construct report
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


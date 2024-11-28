import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from models.content import Content
import time

class FinancialNewsGenerator:
    def __init__(self):
        # Market indices and top stocks mappings
        self.market_stocks = {
            "NYSE": ["AAPL", "MSFT", "V", "JPM", "JNJ"],
            "NASDAQ": ["GOOGL", "AMZN", "NVDA", "META", "TSLA"],
            "Tokyo": ["7203.T", "9984.T", "6758.T", "9433.T", "7267.T"],  # Toyota, Softbank, Sony, NTT, Honda
            "Shanghai": ["600519.SS", "600887.SS", "601398.SS", "600036.SS", "600030.SS"],
            "Hong Kong": ["0700.HK", "9988.HK", "3690.HK", "0941.HK", "0005.HK"],
            "London": ["SHEL.L", "HSBA.L", "BP.L", "ULVR.L", "AZN.L"],
            "Euronext": ["AIR.PA", "OR.PA", "MC.PA", "BNP.PA", "SAN.PA"],
            "Shenzhen": ["000858.SZ", "002572.SZ", "000333.SZ", "000651.SZ", "002415.SZ"]
        }

    def get_stock_data(self, market=None, top_n=5):
        """
        Fetch stock data for a specific market or all markets.

        Args:
            market (str, optional): Specific market to fetch. Defaults to None (all markets).
            top_n (int, optional): Number of top stocks to return per market. Defaults to 5.

        Returns:
            dict: Stock performance data for the specified market or all markets.
        """
        markets_to_fetch = [market] if market else self.market_stocks.keys()
        stock_data = {}

        for market in markets_to_fetch:
            market_stocks = self.market_stocks.get(market, [])
            market_performance = []

            for symbol in market_stocks:
                try:
                    stock = yf.Ticker(symbol)
                    hist = stock.history(period="1d")

                    if not hist.empty:
                        stock_info = {
                            "symbol": symbol,
                            "name": stock.info.get('longName', symbol),
                            "price": hist['Close'].iloc[-1],
                            "change": hist['Close'].iloc[-1] - hist['Open'].iloc[0],
                            "change_percent": ((hist['Close'].iloc[-1] / hist['Open'].iloc[0]) - 1) * 100
                        }
                        market_performance.append(stock_info)

                except Exception as e:
                    print(f"Error fetching data for {symbol}: {e}")

                time.sleep(0.5)

            # Sort and select top_n stocks based on change percentage
            market_performance.sort(key=lambda x: x['change_percent'], reverse=True)
            stock_data[market] = market_performance[:top_n]

        return stock_data

    def create_stock_comparison_chart(self, stock_data):
        """
        Create an interactive stock comparison chart
        
        Args:
            stock_data (dict): Stock performance data
        
        Returns:
            plotly graph object
        """
        # Prepare data for plotting
        fig = go.Figure()

        for market, stocks in stock_data.items():
            # Get stock prices
            for stock in stocks:
                symbol = stock['symbol']
                try:
                    historical_data = yf.Ticker(symbol).history(period="1mo")
                    
                    fig.add_trace(go.Scatter(
                        x=historical_data.index,
                        y=historical_data['Close'],
                        mode='lines',
                        name=f"{market} - {symbol}"
                    ))
                except Exception as e:
                    print(f"Error creating chart for {symbol}: {e}")

        fig.update_layout(
            title='Stock Performance Comparison',
            xaxis_title='Date',
            yaxis_title='Stock Price',
            height=600,
            width=1000,
            legend_title_text='Stocks'
        )

        return fig

    def generate_market_report(self, language="english"):
        """
        Generate a comprehensive market report
        
        Args:
            language (str, optional): Language for the report. Defaults to "english".
        
        Returns:
            Content object with market report
        """
        # Fetch stock data
        stock_data = self.get_stock_data()
        
        # Prepare market report text
        market_summary = f"Global Stock Markets Top Performers ({language.capitalize()}):\n\n"
        
        for market, stocks in stock_data.items():
            market_summary += f"{market} Market Top 5 Stocks:\n"
            for stock in stocks:
                market_summary += (
                    f"  {stock['name']} ({stock['symbol']}):\n"
                    f"    Price: {stock['price']:.2f}\n"
                    f"    Change: {stock['change']:.2f} ({stock['change_percent']:.2f}%)\n"
                )
            market_summary += "\n"

        # Create Content object
        return Content(
            text=market_summary,
            language=language,
            topic="global_stock_markets",
            platform="financial_report"
        )

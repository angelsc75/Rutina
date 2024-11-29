import yfinance as yf
import time
import plotly.graph_objs as go
from models.content import Content

class FinancialNewsGenerator:
    def __init__(self):
        # Inicialización de la clase
        pass

    def get_top_stocks_from_market(self, market_ticker, top_n=5):
        """
        Fetch top stocks for a given market index dynamically.

        Args:
            market_ticker (str): Ticker symbol of the market index (e.g., "^GSPC" for S&P500).
            top_n (int): Number of top stocks to return. Defaults to 5.

        Returns:
            list: List of top stocks with their performance metrics.
        """
        try:
            # Obtener historial del índice de mercado
            market_index = yf.Ticker(market_ticker)
            components = market_index.history(period="1d")

            # Si no hay datos, devolver un mensaje vacío
            if components.empty:
                return []

            top_stocks = []
            for stock_symbol in components.index:
                try:
                    # Obtener datos individuales de las acciones
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

                    # Evitar limitaciones de la API
                    time.sleep(0.5)

                except Exception as e:
                    print(f"Error fetching data for {stock_symbol}: {e}")

            # Ordenar por cambio porcentual y devolver los mejores valores
            top_stocks.sort(key=lambda x: x['change_percent'], reverse=True)
            return top_stocks[:top_n]

        except Exception as e:
            print(f"Error fetching data for market {market_ticker}: {e}")
            return []

    def generate_market_report(self, market_ticker, top_n=5):
        """
        Generate a report for the top stocks in a given market.

        Args:
            market_ticker (str): Ticker symbol of the market index.
            top_n (int): Number of top stocks to include in the report. Defaults to 5.

        Returns:
            str: Market performance summary.
        """
        top_stocks = self.get_top_stocks_from_market(market_ticker, top_n)
        if not top_stocks:
            return f"No data available for market: {market_ticker}"

        report = f"Top {top_n} Stocks in {market_ticker}:\n"
        for stock in top_stocks:
            report += (
                f"  {stock['name']} ({stock['symbol']}):\n"
                f"    Price: ${stock['price']:.2f}\n"
                f"    Change: ${stock['change']:.2f} ({stock['change_percent']:.2f}%)\n"
            )
        return report

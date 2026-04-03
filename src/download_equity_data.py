import yfinance as yf

def get_equity_data():
    ticker = yf.Ticker("AAPL")
    data = ticker.history(period="10y")
    return data
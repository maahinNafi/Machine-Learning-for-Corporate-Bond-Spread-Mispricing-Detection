import yfinance as yf

def get_equity_data(ticker_symbol):
    """
    Pulls historical stock price data for the target company.
    """
    print(f"Fetching equity data for {ticker_symbol}...")
    ticker = yf.Ticker(ticker_symbol)
    # Pulling 5 years to ensure we cover the 2-year ML window + padding
    hist = ticker.history(period="5y")
    return hist


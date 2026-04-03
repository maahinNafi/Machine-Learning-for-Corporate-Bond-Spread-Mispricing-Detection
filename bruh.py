from fredapi import Fred
import os
from dotenv import load_dotenv
import yfinance as yf

load_dotenv()
# Initialize fredapi library with fred api key
fred = Fred(api_key=os.getenv('FRED_API_KEY'))

# BBB Corporate Bond Spread Data
bbb_spread_data = fred.get_series('BAMLC0A4CBBB')

# High Yield Corporate Bond Spread Data
hy_spread_data = fred.get_series('BAMLH0A0HYM2EY')

# 10-Year Treasury Yield
US10Y_data = fred.get_series('DGS10')

# 2-Year Treasury Yield
US2Y_data = fred.get_series('DGS2')

# VIX (Volatility Index)
VIX_data = fred.get_series('VIXCLS')

ticker = yf.Ticker("AAPL")
data = ticker.history(period="10y")
print(data.head())

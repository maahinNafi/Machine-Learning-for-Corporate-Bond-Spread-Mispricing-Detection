from fredapi import Fred
from config import FRED_API_KEY, FRED_SERIES

fred = Fred(api_key=FRED_API_KEY)

def get_fred_data():
    fred_data = {}
    
    for name, series_id in FRED_SERIES.items():
        fred_data[name] = fred.get_series(series_id)

    return fred_data
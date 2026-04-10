import pandas as pd
from fredapi import Fred
import os
from dotenv import load_dotenv

load_dotenv()


def get_fred_data():
    api_key = os.getenv("FRED_API_KEY")

    # Initialize the connection
    fred = Fred(api_key=api_key)

    # Define our required credit and macro series
    series_map = {
        "bbb_spread": "BAMLC0A4CBBB",
        "vix": "VIXCLS",
        "us10y": "DGS10",
        "us2y": "DGS2"
    }

    print("Requesting real-time series from St. Louis Fed...")

    fred_data = {}
    for name, series_id in series_map.items():
        fred_data[name] = fred.get_series(series_id)

    return fred_data
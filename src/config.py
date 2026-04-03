import os
from dotenv import load_dotenv

load_dotenv()
# Initialize fredapi library with fred api key
FRED_API_KEY = os.getenv("FRED_API_KEY")

# List of all FRED data we are collecting
FRED_SERIES = {
    "bbb_spread": "BAMLC0A4CBBB",
    "hy_spread": "BAMLH0A0HYM2EY",
    "us10y": "DGS10",
    "us2y": "DGS2",
    "vix": "VIXCLS"
}
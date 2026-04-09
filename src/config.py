# Centralized Configuration
FRED_API_KEY = "YOUR_KEY_HERE" # Handled via .env locally

FRED_SERIES = {
    "bbb_spread": "BAMLC0A4CBBB",
    "hy_spread": "BAMLC0A4CHEA", # Added High Yield for future risk-on/off checks
    "vix": "VIXCLS",
    "us10y": "DGS10",
    "us2y": "DGS2"
}
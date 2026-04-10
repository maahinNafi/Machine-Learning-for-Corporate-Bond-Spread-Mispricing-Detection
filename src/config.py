from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
MODELS_DIR = PROJECT_ROOT / "models"

# FRED series to download
FRED_SERIES = {
    "bbb_spread": "BAMLC0A4CBBB",
    "hy_spread":  "BAMLH0A0HYM2EY",
    "vix":        "VIXCLS",
    "us10y":      "DGS10",
    "us2y":       "DGS2",
}

# Target company
DEFAULT_TICKER = "MSFT"

# Model settings
RECENCY_YEARS = 2
TEST_SIZE = 0.2
N_ESTIMATORS = 100
RANDOM_STATE = 42

# Signal settings (in basis points)
SIGNAL_THRESHOLD_BPS = 2.0

# Backtest: approximate modified duration for IG corp bonds (~7yr maturity)
BOND_DURATION = 7.0

import pandas as pd
from src.config import DATA_RAW_DIR, DATA_PROCESSED_DIR
from src.download_fred_data import get_fred_data
from src.download_equity_data import get_equity_data


def download_and_save_raw(ticker: str) -> None:
    """Download FRED and equity data and save raw CSVs to data/raw/."""
    DATA_RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading FRED macro data...")
    fred_data = get_fred_data()
    fred_df = pd.DataFrame(fred_data)
    fred_df.index.name = "Date"
    fred_df.to_csv(DATA_RAW_DIR / "fred_raw.csv")
    print(f"  Saved {len(fred_df)} rows to data/raw/fred_raw.csv")

    print(f"Downloading equity data for {ticker}...")
    equity_df = get_equity_data(ticker)
    equity_df.index.name = "Date"
    equity_df.to_csv(DATA_RAW_DIR / f"{ticker}_equity_raw.csv")
    print(f"  Saved {len(equity_df)} rows to data/raw/{ticker}_equity_raw.csv")


def merge_and_align(ticker: str) -> pd.DataFrame:
    """Load raw CSVs, strip timezones, align on trading days, and save merged CSV."""
    fred_df = pd.read_csv(DATA_RAW_DIR / "fred_raw.csv", index_col=0, parse_dates=True)
    equity_df = pd.read_csv(DATA_RAW_DIR / f"{ticker}_equity_raw.csv", index_col=0, parse_dates=True)

    fred_df.index   = pd.to_datetime(fred_df.index,   utc=True).tz_convert(None).normalize()
    equity_df.index = pd.to_datetime(equity_df.index, utc=True).tz_convert(None).normalize()

    equity_slim = equity_df[["Close", "Volume"]].copy()

    merged = pd.concat([fred_df, equity_slim], axis=1, join="inner")

    merged = merged.ffill().dropna()
    merged.index.name = "Date"

    DATA_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    out_path = DATA_PROCESSED_DIR / "merged.csv"
    merged.to_csv(out_path)
    print(f"Merged dataset saved to {out_path} ({len(merged)} rows, {merged.shape[1]} columns)")

    return merged


def run(ticker: str = "MSFT") -> pd.DataFrame:
    download_and_save_raw(ticker)
    return merge_and_align(ticker)

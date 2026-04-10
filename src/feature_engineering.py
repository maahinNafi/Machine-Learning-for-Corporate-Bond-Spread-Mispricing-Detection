import numpy as np
import pandas as pd
from src.config import DATA_PROCESSED_DIR
from src.calculate_ratios import get_company_ratios


def build_feature_matrix(ticker: str) -> pd.DataFrame:
    df = pd.read_csv(DATA_PROCESSED_DIR / "merged.csv", index_col=0, parse_dates=True)

    df["yield_curve_slope"] = df["us10y"] - df["us2y"]

    for lag in [1, 5, 21]:
        df[f"spread_lag_{lag}d"] = df["bbb_spread"].shift(lag)

    df["spread_chg_21d"] = df["bbb_spread"].diff(21)

    if "hy_spread" in df.columns:
        df["hy_spread_lag_1d"] = df["hy_spread"].shift(1)

    df["vix_lag_1d"] = df["vix"].shift(1)

    equity_returns = df["Close"].pct_change()
    for window in [21, 63]:
        df[f"equity_vol_{window}d"] = equity_returns.rolling(window).std() * np.sqrt(252)

    df["equity_mom_1m"] = df["Close"].pct_change(21)
    df["equity_mom_3m"] = df["Close"].pct_change(63)

    
    df = df.drop(columns=["Close", "Volume"], errors="ignore")

    
    print(f"Fetching company ratios for {ticker}...")
    ratios = get_company_ratios(ticker)
    df["interest_coverage"] = ratios["interest_coverage"]
    df["debt_to_equity"] = ratios["debt_to_equity"]

    
    df = df.ffill().dropna()

    out_path = DATA_PROCESSED_DIR / "features.csv"
    df.to_csv(out_path)
    print(f"Feature matrix saved to {out_path} ({len(df)} rows, {df.shape[1]} columns)")

    return df


def run(ticker: str = "MSFT") -> pd.DataFrame:
    return build_feature_matrix(ticker)

import joblib
import numpy as np
import pandas as pd

from src.config import DATA_PROCESSED_DIR, MODELS_DIR, SIGNAL_THRESHOLD_BPS


def load_model():
    path = MODELS_DIR / "spread_model.pkl"
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}. Run train_spread_model first.")
    return joblib.load(path)


def load_test_data():
    x_path = DATA_PROCESSED_DIR / "X_test.csv"
    y_path = DATA_PROCESSED_DIR / "y_test.csv"
    if not x_path.exists() or not y_path.exists():
        raise FileNotFoundError("Test data not found. Run train_spread_model first.")
    X_test = pd.read_csv(x_path, index_col=0, parse_dates=True)
    y_test = pd.read_csv(y_path, index_col=0, parse_dates=True).squeeze("columns")
    return X_test, y_test


def run() -> pd.DataFrame:
    model = load_model()
    X_test, y_test = load_test_data()

    # Predict fair (model) spread
    y_pred = pd.Series(model.predict(X_test), index=X_test.index, name="fair_spread")

    # Mispricing in bps:
    # FRED spreads are in % (e.g. 1.2 = 1.2% = 120 bps), so multiply difference by 100
    # Positive = actual > predicted → bond is CHEAP (market charging too much for risk → BUY)
    # Negative = actual < predicted → bond is RICH (market undercharging for risk → SELL)
    mispricing_bps = (y_test - y_pred) * 100

    # Classify signal
    conditions = [
        mispricing_bps >  SIGNAL_THRESHOLD_BPS,
        mispricing_bps < -SIGNAL_THRESHOLD_BPS,
    ]
    signal = np.select(conditions, ["BUY", "SELL"], default="FLAT")

    signals = pd.DataFrame({
        "actual_spread":    y_test,
        "fair_spread":      y_pred,
        "mispricing_bps":   mispricing_bps,
        "signal":           signal,
    }, index=y_test.index)

    out_path = DATA_PROCESSED_DIR / "signals.csv"
    signals.to_csv(out_path)
    print(f"Signals saved to {out_path}")
    print(pd.Series(signal).value_counts().rename("count"))

    return signals

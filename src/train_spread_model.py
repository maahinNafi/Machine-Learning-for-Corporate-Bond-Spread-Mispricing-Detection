import joblib
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from src.config import (
    DATA_PROCESSED_DIR, MODELS_DIR,
    N_ESTIMATORS, RANDOM_STATE, RECENCY_YEARS, TEST_SIZE,
)


def load_features() -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED_DIR / "features.csv", index_col=0, parse_dates=True)


def apply_recency_filter(df: pd.DataFrame) -> pd.DataFrame:
    """Keep only the last RECENCY_YEARS of data so snapshot ratios stay relevant."""
    cutoff = df.index.max() - pd.Timedelta(days=365 * RECENCY_YEARS)
    filtered = df[df.index > cutoff].copy()
    if len(filtered) < 200:
        raise ValueError(
            f"Only {len(filtered)} rows after recency filter — not enough data to train. "
            "Try increasing RECENCY_YEARS in config.py."
        )
    return filtered


def chronological_split(df: pd.DataFrame):
    """80/20 time-ordered split. No shuffling — preserves temporal integrity."""
    drop_cols = [c for c in ["bbb_spread", "hy_spread"] if c in df.columns]
    X = df.drop(columns=drop_cols)
    y = df["bbb_spread"]
    return train_test_split(X, y, test_size=TEST_SIZE, shuffle=False)


def train(X_train: pd.DataFrame, y_train: pd.Series) -> RandomForestRegressor:
    model = RandomForestRegressor(n_estimators=N_ESTIMATORS, random_state=RANDOM_STATE)
    print(f"Training Random Forest on {len(X_train)} samples...")
    model.fit(X_train, y_train)
    return model


def evaluate(model, X_test: pd.DataFrame, y_test: pd.Series) -> dict:
    preds = model.predict(X_test)
    return {
        "r2":  r2_score(y_test, preds),
        "mae": mean_absolute_error(y_test, preds),
    }


def run() -> tuple:
    df = load_features()
    df = apply_recency_filter(df)

    X_train, X_test, y_train, y_test = chronological_split(df)
    print(f"Train: {len(X_train)} rows | Test: {len(X_test)} rows")

    model = train(X_train, y_train)
    metrics = evaluate(model, X_test, y_test)
    print(f"R²: {metrics['r2']:.4f} | MAE: {metrics['mae']:.4f} %")

    # Save model
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODELS_DIR / "spread_model.pkl"
    joblib.dump(model, model_path)
    print(f"Model saved to {model_path}")

    # Save test split so generate_signals can load it without re-splitting
    X_test.to_csv(DATA_PROCESSED_DIR / "X_test.csv")
    y_test.to_csv(DATA_PROCESSED_DIR / "y_test.csv", header=True)

    return model, metrics

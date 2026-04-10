from src.config import DEFAULT_TICKER
from src.clean_merge_data import run as clean_merge
from src.feature_engineering import run as build_features
from src.train_spread_model import run as train_model
from src.generate_signals import run as generate_signals
from src.backtest_strategy import run as backtest

TICKER = DEFAULT_TICKER

print("=" * 55)
print(f"  Bond Mispricing Detection — {TICKER}")
print("=" * 55)

print("\n[1/5] Downloading & merging data...")
clean_merge(TICKER)

print("\n[2/5] Engineering features...")
build_features(TICKER)

print("\n[3/5] Training spread model...")
_, metrics = train_model()
print(f"      R²: {metrics['r2']:.4f}  |  MAE: {metrics['mae']:.4f} %")

print("\n[4/5] Generating trading signals...")
generate_signals()

print("\n[5/5] Running backtest...")
backtest(TICKER)

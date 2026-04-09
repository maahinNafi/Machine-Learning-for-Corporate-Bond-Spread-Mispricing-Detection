from src.download_fred_data import get_fred_data
from src.build_dataset import create_training_data
from src.train_model import prepare_data_for_ml, train_bond_model, evaluate_model, detect_mispricing
from src.visualize import plot_mispricing

TICKER = "MSFT"

# 1. Pull macro data from FRED
fred_data = get_fred_data()

# 2. Build the training dataset (joins macro + company ratios)
df = create_training_data(fred_data, TICKER)
print(df.tail())

# 3. Prepare, train, evaluate
X_train, X_test, y_train, y_test = prepare_data_for_ml(df)
model = train_bond_model(X_train, y_train)
r2, mae = evaluate_model(model, X_test, y_test)
print(f"R²: {r2:.4f} | MAE: {mae:.4f}")

# 4. Detect mispricing and plot
signals = detect_mispricing(model, X_test, y_test)
print(signals.head(10))
plot_mispricing(signals)

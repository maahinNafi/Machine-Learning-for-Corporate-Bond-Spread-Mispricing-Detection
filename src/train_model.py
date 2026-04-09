from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error
import pandas as pd

# --- TOOL 1: The Preparer ---
import pandas as pd
from sklearn.model_selection import train_test_split


def prepare_data_for_ml(master_df):
    # 1. THE FIX: Filter for the last 2 years only
    # This ensures our 'Snapshot' ratios match the 'Market' reality
    two_years_ago = master_df.index.max() - pd.Timedelta(days=730)
    master_df = master_df[master_df.index > two_years_ago].copy()

    # 2. Define Target and Features
    y = master_df['bbb_spread']

    cols_to_drop = ['bbb_spread']
    if 'hy_spread' in master_df.columns:
        cols_to_drop.append('hy_spread')

    X = master_df.drop(columns=cols_to_drop)

    # 3. Split the data (shorter window, higher quality)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    return X_train, X_test, y_train, y_test


# --- TOOL 2: The Trainer ---
def train_bond_model(X_train, y_train):
    # Initialize 100 decision trees
    model = RandomForestRegressor(n_estimators=100, random_state=42)

    print("Feeding 30 years of history into the Random Forest...")
    model.fit(X_train, y_train)

    return model


# --- TOOL 3: The Grader ---
def evaluate_model(model, X_test, y_test):
    # Make predictions on the data the model has never seen
    predictions = model.predict(X_test)

    # Calculate how accurate we are
    r2 = r2_score(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)

    return r2, mae



def detect_mispricing(model, X_test, y_test):
    # 1. Get the "Fair Value" predictions
    preds = model.predict(X_test)

    # 2. Build a comparison table
    results = pd.DataFrame({
        'Actual_Spread': y_test,
        'Predicted_Fair_Value': preds
    }, index=y_test.index)

    # 3. Calculate the 'Mispricing' (The Residual)
    results['Mispricing_Bps'] = (results['Actual_Spread'] - results['Predicted_Fair_Value']) * 100

    # 4. Identify the "Cheapest" and "Dearest" moments
    # Positive = Cheap (Market is over-charging for risk)
    # Negative = Rich (Market is under-charging for risk)
    return results.sort_values(by='Mispricing_Bps', ascending=False)
import pandas as pd
from src.calculate_ratios import get_company_ratios


def create_training_data(fred_data, ticker_symbol):
    """
    Combines Daily Macro data with Company Health ratios.
    """
    # 1. FRED dict → DataFrame
    df = pd.DataFrame(fred_data)
    df.index = pd.to_datetime(df.index)

    # 2. Micro ratios (point-in-time snapshot)
    ratios = get_company_ratios(ticker_symbol)
    df['interest_coverage'] = ratios['interest_coverage']
    df['debt_to_equity'] = ratios['debt_to_equity']

    # 3. Yield curve slope (classic recession signal)
    if 'us10y' in df.columns and 'us2y' in df.columns:
        df['yield_curve_slope'] = df['us10y'] - df['us2y']

    # 4. Lagged spread (autoregressive baseline)
    df['spread_lag_1'] = df['bbb_spread'].shift(1)

    # 5. Clean up
    df = df.ffill().dropna()

    return df
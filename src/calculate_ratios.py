import yfinance as yf
import pandas as pd


def get_company_ratios(ticker_symbol):
    """
    Takes a ticker symbol and returns key credit ratios
    using the 'Value Hunter' logic to avoid NaNs.
    """
    # 1. Connect to the company
    ticker = yf.Ticker(ticker_symbol)

    # 2. Get the tables
    income = ticker.financials
    balance = ticker.balance_sheet

    # 3. Use the 'Value Hunter' logic for robust data gathering
    # We find the first real number in the row, skipping the 'NaNs'
    ebit = income.loc['EBIT'].dropna().iloc[0]
    interest = income.loc['Interest Expense'].dropna().iloc[0]
    debt = balance.loc['Total Debt'].dropna().iloc[0]
    equity = balance.loc['Stockholders Equity'].dropna().iloc[0]

    # 4. Calculate the two key metrics
    # We use abs() because interest is sometimes reported as a negative number
    interest_coverage = ebit / abs(interest)
    debt_to_equity = debt / equity

    # 5. Return them as a dictionary (a neat package of data)
    return {
        "interest_coverage": round(interest_coverage, 2),
        "debt_to_equity": round(debt_to_equity, 2)
    }

# Machine Learning for Corporate Bond Spread Mispricing Detection

This project uses macroeconomic, equity market, and company financial features to estimate the fair value of corporate bond credit spreads. The notebook compares the actual BBB credit spread against a model-predicted fair spread, identifies potential mispricing, generates BUY / SELL / FLAT signals, and backtests a simple spread-based strategy.

## Project Structure

```text
bond-mispricing/
├── notebooks/
│   └── bond_mispricing_project.ipynb
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Workflow

```text
1. Import libraries and load environment variables
2. Download FRED macro data
3. Download equity data from yfinance
4. Merge and clean macro + equity data
5. Add company financial ratios
6. Engineer model features
7. Run VIF analysis for multicollinearity
8. Drop high-VIF features
9. Train Random Forest spread model
10. Generate BUY / SELL / FLAT mispricing signals
11. Backtest the strategy
12. Visualize mispricing, returns, drawdown, and feature importance
```

## Data Sources

- FRED: corporate bond spreads, Treasury yields, and VIX
- yfinance: equity prices, volume, and company financial statements

## Setup

Clone the repository and install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file in the root folder:

```bash
cp .env.example .env
```

Then add your FRED API key:

```text
FRED_API_KEY=your_fred_api_key_here
```

Do **not** commit your real `.env` file.

## Running the Notebook

Open:

```text
notebooks/bond_mispricing_project.ipynb
```

Then run the cells from top to bottom.

## Notes

This is a research prototype, not financial advice. The strategy is simplified and uses spread changes with an approximate bond duration assumption. Real fixed-income trading would require transaction costs, liquidity constraints, bid-ask spreads, bond-specific spread data, and more robust out-of-sample testing.

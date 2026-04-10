import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.config import DATA_PROCESSED_DIR, BOND_DURATION


def load_signals() -> pd.DataFrame:
    path = DATA_PROCESSED_DIR / "signals.csv"
    if not path.exists():
        raise FileNotFoundError("signals.csv not found. Run generate_signals first.")
    return pd.read_csv(path, index_col=0, parse_dates=True).sort_index()


def simulate_strategy(signals: pd.DataFrame) -> pd.DataFrame:
    df = signals.copy()

    # Daily spread change (in percent units, e.g. 0.05 = 5 bps)
    df["delta_spread"] = df["actual_spread"].diff()

    # Bond return approximation:
    #   return ≈ -duration × (Δspread / 100)
    # The /100 converts from percent to decimal (FRED series is in %)
    df["bond_return"] = -BOND_DURATION * (df["delta_spread"] / 100)

    # Map signal to numeric position
    position_map = {"BUY": 1.0, "SELL": -1.0, "FLAT": 0.0}
    df["position"] = df["signal"].map(position_map)

    # Shift position by 1 day — signal on day t is only actionable on day t+1
    df["position"] = df["position"].shift(1)

    # Drop the first row (NaN from diff + shift)
    df = df.dropna()

    # Daily strategy P&L
    df["strategy_return"]   = df["position"] * df["bond_return"]
    df["benchmark_return"]  = df["bond_return"]  # always-long buy-and-hold

    # Cumulative growth of $1
    df["strategy_cumulative"]  = (1 + df["strategy_return"]).cumprod()
    df["benchmark_cumulative"] = (1 + df["benchmark_return"]).cumprod()

    return df


def compute_metrics(portfolio: pd.DataFrame) -> dict:
    strat = portfolio["strategy_return"]
    n_days = len(strat)

    def sharpe(returns):
        std = returns.std()
        return (returns.mean() / std) * np.sqrt(252) if std > 0 else float("nan")

    def max_drawdown(cumulative):
        roll_max = cumulative.cummax()
        return ((cumulative - roll_max) / roll_max).min()

    active_days = strat[strat != 0]
    win_rate = (active_days > 0).sum() / len(active_days) if len(active_days) > 0 else float("nan")

    total_return = portfolio["strategy_cumulative"].iloc[-1] - 1

    return {
        "total_return":    total_return,
        "annualized_return": (1 + total_return) ** (252 / n_days) - 1,
        "sharpe_ratio":    sharpe(strat),
        "max_drawdown":    max_drawdown(portfolio["strategy_cumulative"]),
        "win_rate":        win_rate,
        "benchmark_return": portfolio["benchmark_cumulative"].iloc[-1] - 1,
        "benchmark_sharpe": sharpe(portfolio["benchmark_return"]),
    }


def plot_results(portfolio: pd.DataFrame, metrics: dict, ticker: str = "MSFT") -> None:
    fig, axes = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

    # --- Panel 1: Actual spread vs fair value with shading ---
    ax = axes[0]
    ax.plot(portfolio.index, portfolio["actual_spread"], label="Actual Spread", color="steelblue", lw=1.5)
    ax.plot(portfolio.index, portfolio["fair_spread"],   label="Model Fair Value", color="darkorange", lw=1.5, linestyle="--")
    ax.fill_between(portfolio.index,
                    portfolio["actual_spread"], portfolio["fair_spread"],
                    where=(portfolio["actual_spread"] > portfolio["fair_spread"]),
                    color="green", alpha=0.25, label="Cheap (BUY zone)")
    ax.fill_between(portfolio.index,
                    portfolio["actual_spread"], portfolio["fair_spread"],
                    where=(portfolio["actual_spread"] < portfolio["fair_spread"]),
                    color="red", alpha=0.25, label="Rich (SELL zone)")
    ax.set_title(f"{ticker} Bond: Actual vs Predicted Fair Spread")
    ax.set_ylabel("Spread (%)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # --- Panel 2: Cumulative returns ---
    ax = axes[1]
    ax.plot(portfolio.index, portfolio["strategy_cumulative"],  label="Strategy", color="steelblue", lw=1.5)
    ax.plot(portfolio.index, portfolio["benchmark_cumulative"], label="Buy & Hold", color="gray",      lw=1.2, linestyle="--")
    ax.axhline(1, color="black", lw=0.8, linestyle=":")
    ax.set_title(
        f"Cumulative Returns  |  Sharpe: {metrics['sharpe_ratio']:.2f}  |  "
        f"Max DD: {metrics['max_drawdown']:.1%}"
    )
    ax.set_ylabel("Growth of $1")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    # --- Panel 3: Drawdown ---
    ax = axes[2]
    roll_max = portfolio["strategy_cumulative"].cummax()
    drawdown = (portfolio["strategy_cumulative"] - roll_max) / roll_max
    ax.fill_between(portfolio.index, drawdown, 0, color="red", alpha=0.4, label="Drawdown")
    ax.set_title("Strategy Drawdown")
    ax.set_ylabel("Drawdown")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)

    fig.suptitle(f"{ticker} Bond Mispricing Strategy — Backtest Results", fontsize=13, fontweight="bold")
    plt.tight_layout()

    out_path = f"backtest_{ticker}.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"Chart saved to {out_path}")


def run(ticker: str = "MSFT") -> dict:
    signals  = load_signals()
    portfolio = simulate_strategy(signals)
    metrics  = compute_metrics(portfolio)

    print("\n--- Backtest Results ---")
    print(f"  Total Return:      {metrics['total_return']:.2%}")
    print(f"  Annualized Return: {metrics['annualized_return']:.2%}")
    print(f"  Sharpe Ratio:      {metrics['sharpe_ratio']:.2f}")
    print(f"  Max Drawdown:      {metrics['max_drawdown']:.2%}")
    print(f"  Win Rate:          {metrics['win_rate']:.2%}")
    print(f"  Benchmark Return:  {metrics['benchmark_return']:.2%}")
    print(f"  Benchmark Sharpe:  {metrics['benchmark_sharpe']:.2f}")

    plot_results(portfolio, metrics, ticker)
    return metrics

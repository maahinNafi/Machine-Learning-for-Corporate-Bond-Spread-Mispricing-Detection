import matplotlib.pyplot as plt


def plot_mispricing(signals):
    signals = signals.sort_index()
    plt.figure(figsize=(12, 6))

    # 1. Plot the two lines
    plt.plot(signals.index, signals['Actual_Spread'], label='Actual Market Spread', color='blue', alpha=0.6)
    plt.plot(signals.index, signals['Predicted_Fair_Value'], label='Model Fair Value', color='orange', linestyle='--')

    # 2. Add the "Mispricing" area
    # This shades the gap between the two lines
    plt.fill_between(signals.index, signals['Actual_Spread'], signals['Predicted_Fair_Value'],
                     where=(signals['Actual_Spread'] > signals['Predicted_Fair_Value']),
                     color='green', alpha=0.3, label='Cheap (Buy)')

    plt.fill_between(signals.index, signals['Actual_Spread'], signals['Predicted_Fair_Value'],
                     where=(signals['Actual_Spread'] < signals['Predicted_Fair_Value']),
                     color='red', alpha=0.3, label='Rich (Sell)')

    plt.title('MSFT Bond Mispricing: Market Spread vs. Model Fair Value (April 2026)')
    plt.ylabel('Spread (%)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()
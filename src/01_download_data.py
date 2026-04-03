from download_fred_data import get_fred_data
from download_equity_data import get_equity_data

fred_data = get_fred_data()
equity_data = get_equity_data()

print(fred_data)
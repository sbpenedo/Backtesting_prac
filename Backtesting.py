import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# Fetching data
ticker = 'SPY'
start_date = '2010-01-01'
# Use the current date for the end date
end_date = pd.Timestamp.now().strftime('%Y-%m-%d')

# Download data
data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    print(f"No data found for {ticker}. Exiting.")
    exit()

print(f"Data for {ticker} fetched successfully:")
print(data.head())
print("-" * 30 )
print()

short_window = 50
long_window = 200

# Create a new DataFrame for our strategy analysis
signals = pd.DataFrame(index=data.index)
signals['price'] = data['Close']

# Calculate Short and Long Simple Moving Averages
signals[f'sma_{short_window}'] = signals['price'].rolling(window=short_window, min_periods=1).mean()
signals[f'sma_{long_window}'] = signals['price'].rolling(window=long_window, min_periods=1).mean()

# Create a column to represent our position in the market (1 for long, 0 for neutral)
# We are long when the short SMA is above the long SMA
signals['position'] = np.where(signals[f'sma_{short_window}'] > signals[f'sma_{long_window}'], 1.0, 0.0)

# Calculate the crossovers
# A '1' indicates a Golden Cross (buy signal: position changed from 0 to 1)
# A '-1' indicates a Death Cross (sell signal: position changed from 1 to 0)
signals['signal'] = signals['position'].diff()

print("Signals generated:")
print(signals.tail())
# Check trade signals
print("\nBuy/Sell signals:")
print(signals[signals['signal'] != 0].head())
print("-" * 30, "\n")

print("Running backtesting simulation...")
initial_capital = 100000.0

# Create a portfolio DataFrame
portfolio = pd.DataFrame(index=signals.index).fillna(0.0)
# Check DataFrame
print(portfolio.head())

# Our holdings start with the initial capital
portfolio['cash'] = initial_capital
# Store the value of our stock position
portfolio['holdings'] = 0.0
# Sum of cash and holdings
portfolio['total'] = initial_capital

# Check DataFrame
print(portfolio.head())

# Tracks the number of shares we own
position_size = 0

# Loop through the data to simulate trading
for i in range(1, len(signals)):
    # Copy previous day's values
    portfolio.loc[signals.index[i], 'cash'] = portfolio.loc[signals.index[i-1], 'cash']
    portfolio.loc[signals.index[i], 'holdings'] = portfolio.loc[signals.index[i-1], 'holdings']

    # If we get a BUY signal and we are not already in the market
    if signals['signal'].iloc[i] == 1.0 and position_size == 0:
        # Buy as many shares as possible
        current_price = signals['price'].iloc[i]
        shares_to_buy = portfolio['cash'].iloc[i] // current_price
        position_size = shares_to_buy
        
        # Update cash and holdings
        cost = shares_to_buy * current_price
        portfolio.loc[signals.index[i], 'cash'] -= cost
        portfolio.loc[signals.index[i], 'holdings'] = shares_to_buy * current_price
        print(f"{signals.index[i].date()}: BUY {int(shares_to_buy)} shares at ${current_price:.2f}")

    # If we get a SELL signal and we are currently in the market
    elif signals['signal'].iloc[i] == -1.0 and position_size > 0:
        # Sell all shares
        current_price = signals['price'].iloc[i]
        revenue = position_size * current_price
        
        # Update cash and holdings
        portfolio.loc[signals.index[i], 'cash'] += revenue
        portfolio.loc[signals.index[i], 'holdings'] = 0.0
        print(f"{signals.index[i].date()}: SELL {int(position_size)} shares at ${current_price:.2f}")
        position_size = 0
    
    # If there's no trade, just update the value of our current holdings
    else:
        portfolio.loc[signals.index[i], 'holdings'] = position_size * signals['price'].iloc[i]

    # Update total portfolio value
    portfolio.loc[signals.index[i], 'total'] = portfolio['cash'].iloc[i] + portfolio['holdings'].iloc[i]


print("\nBacktest complete. Portfolio summary:")
print(portfolio.tail())
print("-" * 30)
print()

print("Analyzing performance and generating plots...")

# Total Return
final_portfolio_value = portfolio['total'].iloc[-1]
total_return = (final_portfolio_value / initial_capital) - 1
print(f"Total Return: {total_return:.2%}")

# Annualized Return (CAGR: Computer Annual Growth Rate)
days = (portfolio.index[-1] - portfolio.index[0]).days
cagr = ((final_portfolio_value / initial_capital) ** (365.0/days)) - 1
print(f"Annualized Return (CAGR): {cagr:.2%}")

# Sharpe Ratio (Risk-Adjusted Return)
# A higher Sharpe ratio is better, (1.0 good, 2.0 excellent, 3.0 outstanding) 
# ( < 1.0 represents insufficient return for the level of risk taken) 
# Assuming a risk-free rate of 0 for simplicity
portfolio['daily_return'] = portfolio['total'].pct_change(1)
sharpe_ratio = np.sqrt(252) * portfolio['daily_return'].mean() / portfolio['daily_return'].std()
print(f"Sharpe Ratio: {sharpe_ratio:.2f}")

# Max Drawdown
portfolio['rolling_max'] = portfolio['total'].cummax()
portfolio['daily_drawdown'] = (portfolio['total'] / portfolio['rolling_max']) - 1.0
max_drawdown = portfolio['daily_drawdown'].min()
print(f"Maximum Drawdown: {max_drawdown:.2%}")


# Plot Equity Curve (Portfolio Value over Time)
plt.figure(figsize=(12, 6))
plt.plot(portfolio['total'], label='Strategy Equity Curve')
# Also plot a Buy and Hold strategy for comparison
buy_and_hold_return = (data['Close'] / data['Close'].iloc[0]) * initial_capital
plt.plot(buy_and_hold_return, label='Buy and Hold SPY')
plt.title(f'{ticker} Strategy vs. Buy and Hold')
plt.ylabel('Portfolio Value ($)')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.show()

# 2. Plot Price, SMAs, and Trade Signals
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(signals['price'], label='Price')
ax.plot(signals[f'sma_{short_window}'], label=f'{short_window}-Day SMA', color='orange')
ax.plot(signals[f'sma_{long_window}'], label=f'{long_window}-Day SMA', color='purple')

# Plot Buy signals
ax.plot(signals[signals['signal'] == 1.0].index, 
         signals[f'sma_{short_window}'][signals['signal'] == 1.0],
         '^', markersize=12, color='g', label='Buy Signal')

# Plot Sell signals
ax.plot(signals[signals['signal'] == -1.0].index, 
         signals[f'sma_{short_window}'][signals['signal'] == -1.0],
         'v', markersize=12, color='r', label='Sell Signal')

plt.title(f'{ticker} Price with SMA Crossover Signals')
plt.ylabel('Price ($)')
plt.xlabel('Date')
plt.legend()
plt.grid(True)
plt.show()

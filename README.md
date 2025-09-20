# Backtesting_prac

This is my first try at backtesting in Python. I’m teaching myself how to do this, so I’m just experimenting.  
I wanted to see how a simple **moving average crossover strategy** would work on the S&P 500 (SPY).

The script (`backtesting.py`) gets historical price data, figures out buy/sell signals using **Simple Moving Averages (SMAs)**, and simulates trading.  
It also compares how the strategy would do versus just buying and holding SPY.

---

## What I Learned
- How to grab stock data with [`yfinance`](https://pypi.org/project/yfinance/).  
- How to calculate **short** and **long** SMAs.  
- The ideas of:
  - **Golden Cross** (buy: short SMA goes above long SMA)  
  - **Death Cross** (sell: short SMA goes below long SMA)  
- How backtesting works: keeping track of positions, cash, and total portfolio value.  
- How to measure performance with **CAGR**, **Sharpe ratio**, and **max drawdown**.

## Results
<img width="1200" height="600" alt="Figure_1" src="https://github.com/user-attachments/assets/d8705f74-8340-401f-9aab-be0178f43d7f" />


<img width="1344" height="629" alt="Figure_2" src="https://github.com/user-attachments/assets/7aba07f5-24ef-42d3-bbf8-7261669b9a27" />

Total Return: 243.90%

Annualized Return (CAGR): 8.18%

Sharpe Ratio: 0.62

Maximum Drawdown: -33.68%

The strategy didn’t beat just holding the S&P 500, but it was good practice and learning experience.

---

## Requirements
You’ll need Python and these libraries:

```bash
pip install pandas numpy yfinance matplotlib

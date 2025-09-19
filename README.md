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

The strategy didn’t beat just holding the S&P 500, but it was good practice and I learned a lot.

---

## Requirements
You’ll need Python and these libraries:

```bash
pip install pandas numpy yfinance matplotlib

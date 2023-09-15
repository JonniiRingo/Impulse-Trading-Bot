import MetaTrader5 as mt5
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Connect to the MetaTrader 5 trading platform
mt5.initialize()

# Define the currency pair and time frame for analysis
pair = "EURUSD"
time_frame = mt5.TIMEFRAME_M1

# Retrieve the price data for the specified currency pair and time frame
price_data = pd.DataFrame(mt5.copy_rates_from(pair, time_frame, datetime.now(), 1000))

# Calculate the simple moving average over the past 50 bars
price_data['SMA50'] = price_data['close'].rolling(window=50).mean()

# Calculate the simple moving average over the past 200 bars
price_data['SMA200'] = price_data['close'].rolling(window=200).mean()

# Plot the price data and the moving averages
plt.plot(price_data['close'], label='Close Price')
plt.plot(price_data['SMA50'], label='50-bar SMA')
plt.plot(price_data['SMA200'], label='200-bar SMA')
plt.legend()
plt.show()

# Implement the trading strategy
current_price = price_data['close'][-1]
sma50 = price_data['SMA50'][-1]
sma200 = price_data['SMA200'][-1]

if sma50 > sma200 and mt5.account_info().balance > 0:
    # Go long if the 50-bar SMA is above the 200-bar SMA and there is sufficient balance
    mt5.trade.buy(pair, 0.1, current_price)
elif sma50 < sma200 and mt5.account_info().balance > 0:
    # Go short if the 50-bar SMA is below the 200-bar SMA and there is sufficient balance
    mt5.trade.sell(pair, 0.1, current_price)

# Close the connection to the MetaTrader 5 trading platform
mt5.shutdown()

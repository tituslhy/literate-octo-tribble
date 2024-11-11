import yfinance as yf
import pandas as pd
import datetime

# Define the time frame for the past year
end_date = datetime.datetime.now()
start_date = end_date - datetime.timedelta(days=365)

# Download historical stock prices for AAPL
apple_stock_data = yf.download("AAPL", start=start_date, end=end_date)

# Calculate performance indicators
closing_prices = apple_stock_data['Close']
percentage_change = ((closing_prices[-1] - closing_prices[0]) / closing_prices[0]) * 100
highest_price = closing_prices.max()
lowest_price = closing_prices.min()
average_price = closing_prices.mean()

# Print the performance indicators
print(f"Percentage Change: {percentage_change:.2f}%")
print(f"Highest Price: ${highest_price:.2f}")
print(f"Lowest Price: ${lowest_price:.2f}")
print(f"Average Price: ${average_price:.2f}")

# Calculate moving averages
apple_stock_data['50_MA'] = closing_prices.rolling(window=50).mean()
apple_stock_data['200_MA'] = closing_prices.rolling(window=200).mean()

# Print the latest moving averages
latest_50_ma = apple_stock_data['50_MA'].iloc[-1]
latest_200_ma = apple_stock_data['200_MA'].iloc[-1]
print(f"Latest 50-Day MA: ${latest_50_ma:.2f}")
print(f"Latest 200-Day MA: ${latest_200_ma:.2f}")

# Confirm retrieval and display the last few rows of the data
print(apple_stock_data.tail())

# Additional Data: Market Comparison (e.g., S&P 500)
# (Optional: You'll need to add a similar retrieval for S&P 500 or other relevant index)
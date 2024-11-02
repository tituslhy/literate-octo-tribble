import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Define the ticker symbol and date range
ticker_symbol = 'ILMN'
end_date = datetime(2024, 11, 2)
start_date = end_date - timedelta(days=30)

# Fetch historical stock data
data = yf.download(ticker_symbol, start=start_date, end=end_date)

# Calculate percentage change over the month
data['Percentage Change'] = ((data['Close'] - data['Close'].iloc[0]) / data['Close'].iloc[0]) * 100

# Identify the highest and lowest stock prices during this period
highest_price = data['Close'].max()
lowest_price = data['Close'].min()

# Calculate average trading volume
average_volume = data['Volume'].mean()

# Prepare results
result = {
    'start_price': data['Close'].iloc[0],
    'end_price': data['Close'].iloc[-1],
    'percentage_change': data['Percentage Change'].iloc[-1],
    'highest_price': highest_price,
    'lowest_price': lowest_price,
    'average_volume': average_volume
}

print(result)
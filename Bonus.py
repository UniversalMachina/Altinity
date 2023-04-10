import random
from datetime import datetime, timedelta
from clickhouse_driver import Client
import pandas as pd
import numpy as np

"""
This code generated random stock information
Stores it in the clickhouse server
The retrieves the information and prints it


"""

# Initialize ClickHouse client
client = Client('localhost')

# Create a table for stock data
client.execute("""
CREATE TABLE IF NOT EXISTS stock_data (
    symbol String,
    date Date,
    open Float64,
    high Float64,
    low Float64,
    close Float64,
    volume UInt64
) ENGINE = MergeTree()
ORDER BY (symbol, date)
""")

# Function to generate and store synthetic stock data
def generate_and_store_stock_data(symbol, start_date, end_date, start_price, volatility):
    date_format = "%Y-%m-%d"
    start_date = datetime.strptime(start_date, date_format)
    end_date = datetime.strptime(end_date, date_format)

    current_date = start_date
    current_price = start_price
    rows = []

    while current_date <= end_date:
        open_price = current_price
        high_price = open_price + random.uniform(0, open_price * volatility)
        low_price = open_price - random.uniform(0, open_price * volatility)
        close_price = random.uniform(low_price, high_price)
        volume = random.randint(1000, 100000)

        rows.append((symbol, current_date, open_price, high_price, low_price, close_price, volume))

        current_price = close_price
        current_date += timedelta(days=1)

    client.execute(f"INSERT INTO stock_data (symbol, date, open, high, low, close, volume) VALUES", rows)

# Generate and store synthetic stock data
symbol = 'SYNTH'
start_date = '2021-01-01'
end_date = '2021-12-31'
start_price = 100
volatility = 0.05
generate_and_store_stock_data(symbol, start_date, end_date, start_price, volatility)

# Fetch the first 10 rows of synthetic stock data from the ClickHouse database
query_result = client.execute(f"SELECT * FROM stock_data WHERE symbol = '{symbol}' LIMIT 10")

# Convert the result to a pandas DataFrame
columns = ["symbol", "date", "open", "high", "low", "close", "volume"]
stock_data = pd.DataFrame(query_result, columns=columns)

# Print the first 10 rows of the synthetic stock data
print(stock_data)
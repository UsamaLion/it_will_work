import ccxt
import time
import pandas as pd

# List of cryptocurrencies to track
symbols = ['BTC/USDT', 'ETH/USDT', 'ADA/USDT']

# Define the top exchanges to check
exchanges_list = ['binance', 'kraken']

# Create exchange instances
exchanges = {name: getattr(ccxt, name)() for name in exchanges_list}

# Function to fetch prices from each exchange
def fetch_prices():
    prices = {}
    for exchange_name, exchange in exchanges.items():
        prices[exchange_name] = {}
        for symbol in symbols:
            try:
                ticker = exchange.fetch_ticker(symbol)
                prices[exchange_name][symbol] = ticker['last']
            except Exception as e:
                prices[exchange_name][symbol] = f"Error: {str(e)}"
    return prices

# Function to calculate price difference
def calculate_price_difference(row):
    # Collect prices for each exchange
    symbol_prices = [row[exchange] for exchange in exchanges_list if row[exchange] != "Error"]
    if symbol_prices:
        max_price = max(symbol_prices)
        min_price = min(symbol_prices)
        price_diff = max_price - min_price
        return price_diff
    return None

# Function to display prices in a table format and calculate price differences
def display_prices(prices):
    price_data = []
    for symbol in symbols:
        row = {'Symbol': symbol}
        # Collect prices for each exchange
        for exchange_name in exchanges_list:
            row[exchange_name] = prices.get(exchange_name, {}).get(symbol, "Error")
        price_data.append(row)

    # Create a DataFrame from the price data
    df = pd.DataFrame(price_data)
    
    # Add price difference column
    df['Price Difference'] = df.apply(calculate_price_difference, axis=1)
    
    print("\n--- Cryptocurrency Prices ---")
    print(df)
    
# Main loop
try:
    while True:
        prices = fetch_prices()
        display_prices(prices)
        time.sleep(10)  # Update every 60 seconds
except KeyboardInterrupt:
    print("\nExiting the program...")

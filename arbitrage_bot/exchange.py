import requests
import ccxt
from config import EXCHANGES

class Exchange:
    def __init__(self, name):
        self.name = name
        self.api_key = EXCHANGES[name]['api_key']
        self.api_secret = EXCHANGES[name]['api_secret']

    def get_price(self, coin_pair):
        # Implement API calls to get real-time prices
        if self.name == 'binance':
            return self.get_binance_price(coin_pair)
        elif self.name == 'bybit':
            return self.get_bybit_price(coin_pair)
        elif self.name == 'gateio':
            return self.get_gateio_price(coin_pair)
        elif self.name == 'kucoin':
            return self.get_kucoin_price(coin_pair)

    def get_binance_price(self, coin_pair):
        # Example API call for Binance
        url = f'https://api.binance.com/api/v3/ticker/price?symbol={coin_pair.replace("/", "")}'
        response = requests.get(url)
        
        # Log the response for debugging
        print(f"Binance API Response: {response.json()}")  # Log the response
        
        # Check if 'price' is in the response
        if 'price' in response.json():
            return float(response.json()['price'])
        else:
            print("Using ccxt to fetch price due to API failure.")
            return self.get_price_with_ccxt(coin_pair)

    def get_price_with_ccxt(self, coin_pair):
        exchange = ccxt.binance()
        ticker = exchange.fetch_ticker(coin_pair.replace("/", "").lower())
        return ticker['last']

    def get_bybit_price(self, coin_pair):
        exchange = ccxt.bybit()
        ticker = exchange.fetch_ticker(coin_pair.replace("/", "").lower())
        return ticker['last']

    def get_gateio_price(self, coin_pair):
        exchange = ccxt.gateio()
        ticker = exchange.fetch_ticker(coin_pair.replace("/", "").lower())
        return ticker['last']

    def get_kucoin_price(self, coin_pair):
        # Example API call for KuCoin
        url = f'https://api.kucoin.com/api/v1/prices?symbol={coin_pair.replace("/", "-").lower()}'
        response = requests.get(url)
        return float(response.json()['data'][coin_pair.replace("/", "-").lower()])

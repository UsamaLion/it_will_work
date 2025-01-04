# Configuration settings for the arbitrage bot

EXCHANGES = {
    'binance': {
        'api_key': 'YOUR_BINANCE_API_KEY',
        'api_secret': 'YOUR_BINANCE_API_SECRET'
    },
    'bybit': {
        'api_key': 'YOUR_BYBIT_API_KEY',
        'api_secret': 'YOUR_BYBIT_API_SECRET'
    },
    'gateio': {
        'api_key': 'YOUR_GATEIO_API_KEY',
        'api_secret': 'YOUR_GATEIO_API_SECRET'
    },
    'kucoin': {
        'api_key': 'YOUR_KUCOIN_API_KEY',
        'api_secret': 'YOUR_KUCOIN_API_SECRET'
    }
}

COIN_PAIRS = ['BTC/USDT', 'ETH/USDT']  # Customizable coin pairs
PROFIT_THRESHOLD = 0.5  # Minimum profit percentage to trigger alerts
UPDATE_INTERVAL = 60  # Time in seconds to update prices
LOG_FILE = 'arbitrage_opportunities.csv'  # Log file for detected opportunities

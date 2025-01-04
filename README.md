# Arbitrage Cryptocurrency Bot

This project is a cryptocurrency arbitrage bot that scans multiple exchanges to identify arbitrage opportunities based on price differences for the same coin.

## Features
- Connects to multiple cryptocurrency exchanges (Binance, Coinbase, Kraken, KuCoin).
- Retrieves real-time prices for selected coins.
- Detects arbitrage opportunities and calculates potential profit margins.
- Logs detected opportunities in a CSV file.
- Sends real-time notifications via email when an opportunity is found.
- Configurable settings for coin pairs, profit thresholds, and update intervals.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd arbitrage_bot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the bot:**
   - Open `config.py` and enter your API keys for the exchanges.
   - Customize the coin pairs and profit threshold as needed.

4. **Run the bot:**
   ```bash
   python main.py
   ```

## Error Handling
The bot includes error handling for API failures, connection issues, and rate-limiting scenarios.

## License
This project is licensed under the MIT License.

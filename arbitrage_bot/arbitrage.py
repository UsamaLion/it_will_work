from exchange import Exchange
from config import COIN_PAIRS, PROFIT_THRESHOLD, UPDATE_INTERVAL
import time
from prettytable import PrettyTable

class ArbitrageBot:
    def __init__(self):
        self.exchanges = [Exchange(name) for name in ['binance', 'bybit', 'gateio', 'kucoin']]

    def start_monitoring(self):
        while True:
            opportunities = self.detect_arbitrage()
            self.display_prices(opportunities)
            time.sleep(UPDATE_INTERVAL)

    def detect_arbitrage(self):
        prices = {pair: {} for pair in COIN_PAIRS}
        for exchange in self.exchanges:
            for pair in COIN_PAIRS:
                price = exchange.get_price(pair)
                prices[pair][exchange.name] = price

        opportunities = []
        for pair, price_data in prices.items():
            max_price = max(price_data.values())
            min_price = min(price_data.values())
            profit_percentage = ((max_price - min_price) / min_price) * 100

            if profit_percentage >= PROFIT_THRESHOLD:
                opportunities.append({
                    'pair': pair,
                    'max_price': max_price,
                    'min_price': min_price,
                    'profit_percentage': profit_percentage
                })

        return opportunities

    def display_prices(self, opportunities):
        table = PrettyTable()
        table.field_names = ["Coin Pair", "Max Price", "Min Price", "Profit Percentage"]

        for opportunity in opportunities:
            table.add_row([opportunity['pair'], opportunity['max_price'], opportunity['min_price'], f"{opportunity['profit_percentage']:.2f}%"])

        print(table)

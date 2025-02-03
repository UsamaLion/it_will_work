import ccxt.async_support as ccxt
import asyncio
import mysql.connector
from datetime import datetime

class ArbitrageEngine:
    def __init__(self, loop, exchanges=['binance', 'kraken', 'coinbasepro', 'huobi', 'okex', 'bitstamp']):
        self.loop = loop
        self.exchanges = {ex: getattr(ccxt, ex)({
            'enableRateLimit': True,
            'asyncio_loop': self.loop,
            'dns_resolver': False
        }) for ex in exchanges}
        self.coins = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT']  # Start with 3 coins for testing
        self.scan_progress = 0
        self.db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='crypto_arbitrage'
        )

    async def fetch_prices(self, coin_pair):
        prices = {}
        for exchange_name, exchange in self.exchanges.items():
            try:
                ticker = await exchange.fetch_ticker(coin_pair)
                prices[exchange_name] = ticker['last']
                await exchange.close()
            except Exception as e:
                print(f"Error fetching {exchange_name}: {str(e)}")
        return prices

    def calculate_arbitrage(self, prices, coin_pair):
        opportunities = []
        if len(prices) < 2:
            return opportunities

        sorted_prices = sorted(prices.items(), key=lambda x: x[1])
        lowest_ex, lowest_price = sorted_prices[0]
        highest_ex, highest_price = sorted_prices[-1]

        price_diff = highest_price - lowest_price
        fees = (lowest_price * 0.001) + (highest_price * 0.001)
        net_profit = price_diff - fees

        if net_profit > 0:
            opportunities.append({
                'exchange_from': lowest_ex,
                'exchange_to': highest_ex,
                'coin_pair': coin_pair,
                'buy_price': lowest_price,
                'sell_price': highest_price,
                'price_diff': price_diff,
                'fees': fees,
                'net_profit': net_profit,
                'timestamp': datetime.now()
            })
        return opportunities

    async def run_scan(self):
        total_coins = len(self.coins)
        for index, coin in enumerate(self.coins):
            try:
                prices = await self.fetch_prices(coin)
                opportunities = self.calculate_arbitrage(prices, coin)
                if opportunities:
                    self.save_opportunities(opportunities)
                
                # Update progress
                self.scan_progress = int((index + 1) / total_coins * 100)
                await asyncio.sleep(1)  # Rate limit
            except Exception as e:
                print(f"Error scanning {coin}: {str(e)}")

    async def run(self):
        while True:
            await self.run_scan()
            await asyncio.sleep(60)  # Rescan every 60 seconds

    def save_opportunities(self, opportunities):
        cursor = self.db.cursor()
        sql = """
        INSERT INTO arbitrage_opportunities 
        (timestamp, exchange_from, exchange_to, coin_pair, price_diff, fees, net_profit, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending')
        """
        for opp in opportunities:
            cursor.execute(sql, (
                opp['timestamp'],
                opp['exchange_from'],
                opp['exchange_to'],
                opp['coin_pair'],
                opp['price_diff'],
                opp['fees'],
                opp['net_profit']
            ))
        self.db.commit()
        cursor.close()

    def get_scan_progress(self):
        return self.scan_progress
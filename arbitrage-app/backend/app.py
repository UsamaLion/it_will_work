from flask import Flask, render_template, jsonify
from arbitrage_engine import ArbitrageEngine
import asyncio
import mysql.connector
from threading import Thread, Event
import sys
import atexit
from decimal import Decimal

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)
engine = None
stop_event = Event()

def cleanup():
    global stop_event
    stop_event.set()
    print("\nShutting down exchanges...")
    if engine:
        for ex in engine.exchanges.values():
            try:
                asyncio.run(ex.close())
            except:
                pass

atexit.register(cleanup)

def start_arbitrage_engine():
    global engine
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    engine = ArbitrageEngine(loop=loop)
    
    try:
        while not stop_event.is_set():
            loop.run_until_complete(engine.run())
    finally:
        loop.close()

Thread(target=start_arbitrage_engine, daemon=True).start()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/prices')
async def get_prices():
    try:
        if not engine:
            return jsonify([])
            
        prices = {}
        valid_exchanges = []
        
        # Get prices for BTC/USDT across all exchanges
        for ex_name, ex in engine.exchanges.items():
            try:
                ticker = await ex.fetch_ticker('BTC/USDT')
                prices[ex_name] = float(ticker['last'])
                valid_exchanges.append(ex_name)
                await ex.close()
            except Exception as e:
                print(f"Error fetching {ex_name}: {str(e)}")
                continue
        
        if not valid_exchanges:
            return jsonify([])

        sorted_prices = sorted(prices.items(), key=lambda x: x[1])
        avg_price = sum(prices.values()) / len(prices)
        
        return jsonify([{
            'name': name,
            'price': price,
            'difference': ((price - avg_price) / avg_price) * 100,
            'recommendation': 'Buy' if price == sorted_prices[0][1] else 'Sell' if price == sorted_prices[-1][1] else '-'
        } for name, price in prices.items()])
    
    except Exception as e:
        print(f"API Error: {str(e)}")
        return jsonify([])

@app.route('/api/opportunities')
def get_opportunities():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='crypto_arbitrage'
        )
        cursor = db.cursor(dictionary=True)
        
        # Get last 50 opportunities regardless of time
        cursor.execute("""
            SELECT * FROM arbitrage_opportunities 
            ORDER BY timestamp DESC
            LIMIT 50
        """)
        data = cursor.fetchall()
        cursor.close()
        
        # Convert Decimal types to float
        for item in data:
            for key in ['net_profit', 'fees', 'price_diff']:
                if isinstance(item[key], Decimal):
                    item[key] = float(item[key])
            # Add missing fields for frontend
            item['buy_price'] = float(item['price_diff'] - item['net_profit'] - item['fees'])
            item['sell_price'] = float(item['price_diff'] + item['net_profit'])
        
        return jsonify(data)
    except Exception as e:
        print(f"Database error: {str(e)}")
        return jsonify([])

if __name__ == '__main__':
    app.run(debug=True)
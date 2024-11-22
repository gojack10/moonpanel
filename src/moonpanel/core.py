import asyncio
import json
import pytz
from datetime import datetime
from websockets import connect
from termcolor import cprint
from collections import defaultdict

class MoonPanel:
    def __init__(self, show_percent=False, show_ratio=False):
        self.show_percent = show_percent
        self.show_ratio = show_ratio
        self.symbols = ['btcusdt']
        self.websocket_url_base = 'wss://fstream.binance.com/ws/'
        self.trade_counts = defaultdict(lambda: {'buys': 0, 'sells': 0})
        self.last_prices = defaultdict(float)
        self.IMPACT_DELAY = 2

    async def binance_trade_stream(self, uri, symbol):
        try:
            async with connect(uri, close_timeout=0) as websocket:
                while True:
                    try:
                        message = await websocket.recv()
                        data = json.loads(message)
                        
                        price = float(data['p'])
                        is_buyer = data['m'] == False
                        timestamp = datetime.fromtimestamp(data['T'] / 1000, tz=pytz.UTC).strftime('%H:%M:%S')
                        
                        # Update trade counts
                        if is_buyer:
                            self.trade_counts[symbol]['buys'] += 1
                        else:
                            self.trade_counts[symbol]['sells'] += 1
                        
                        # Update last price
                        self.last_prices[symbol] = price
                        
                        # Display trade
                        self.display_trade(symbol, price, is_buyer, timestamp)
                        
                    except asyncio.CancelledError:
                        await websocket.close()
                        return
                    except Exception as e:
                        print(f"Error: {e}")
                        try:
                            await asyncio.sleep(5)
                        except asyncio.CancelledError:
                            await websocket.close()
                            return
        except asyncio.CancelledError:
            return  # Exit cleanly on cancellation

    def display_trade(self, symbol, price, is_buy, timestamp):
        symbol = symbol.replace('usdt', '').upper()
        trade_str = f"{' BUY' if is_buy else 'SELL'} {symbol} {timestamp} {price:.2f} USD"
        
        if self.show_percent:
            percent_change = self.calculate_percent_change(symbol, price)
            trade_str += f" │ {percent_change:+.6f}%"
        
        if self.show_ratio:
            buy_ratio, sell_ratio = self.calculate_ratios(symbol)
            trade_str += f" │ {buy_ratio:.1f}% Buys / {sell_ratio:.1f}% Sells"
        
        # Determine color and formatting based on price
        color = 'green' if is_buy else 'red'
        attrs = ['bold'] if price >= 50000 else []
        
        if price >= 500000:
            prefix = '**'
            color = 'blue' if is_buy else 'magenta'
        else:
            prefix = '*'
        
        # Display with background color
        cprint(f"{prefix}{trade_str}", 'white', f'on_{color}', attrs=attrs)

    def calculate_percent_change(self, symbol, current_price):
        previous_price = self.last_prices[symbol.lower() + 'usdt']
        if previous_price == 0:
            return 0.0
        return ((current_price - previous_price) / previous_price) * 100

    def calculate_ratios(self, symbol):
        symbol = symbol.lower() + 'usdt'
        total = self.trade_counts[symbol]['buys'] + self.trade_counts[symbol]['sells']
        if total == 0:
            return 0.0, 0.0
        buy_ratio = (self.trade_counts[symbol]['buys'] / total) * 100
        sell_ratio = (self.trade_counts[symbol]['sells'] / total) * 100
        return buy_ratio, sell_ratio

    async def run(self):
        try:
            tasks = [
                self.binance_trade_stream(f"{self.websocket_url_base}{symbol}@aggTrade", symbol)
                for symbol in self.symbols
            ]
            await asyncio.gather(*tasks, return_exceptions=True)
        except asyncio.CancelledError:
            pass

    async def cleanup(self):
        """Cleanup resources before shutdown."""
        # Add any cleanup logic here if needed
        pass

# Move the direct execution code into the class
# Remove or comment out: asyncio.run(main())

# If you have a main() function in core.py, wrap it like this:
if __name__ == '__main__':
    asyncio.run(main())
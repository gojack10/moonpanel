import asyncio
import argparse
from .core import MoonPanel

def main():
    parser = argparse.ArgumentParser(description='MoonPanel - Crypto Trade Monitor')
    parser.add_argument('-p', '--percent', action='store_true', help='Show price percent change')
    parser.add_argument('-r', '--ratio', action='store_true', help='Show buy/sell ratio')
    
    args = parser.parse_args()
    
    panel = MoonPanel(show_percent=args.percent, show_ratio=args.ratio)
    asyncio.run(panel.run())

if __name__ == '__main__':
    main()
import asyncio
import argparse
import signal
from core import MoonPanel

async def shutdown(signal, loop, panel):
    """Cleanup tasks tied to the service's shutdown."""
    print(f"\nReceived exit signal {signal.name}...")
    
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    
    print("Cancelling outstanding tasks...")
    for task in tasks:
        task.cancel()
    
    try:
        await asyncio.gather(*tasks, return_exceptions=True)
    except Exception:
        pass
    
    loop.stop()

def main():
    parser = argparse.ArgumentParser(description='MoonPanel - Crypto Trade Monitor')
    parser.add_argument('-p', '--percent', action='store_true', help='Show price percent change')
    parser.add_argument('-r', '--ratio', action='store_true', help='Show buy/sell ratio')
    
    args = parser.parse_args()
    
    panel = MoonPanel(show_percent=args.percent, show_ratio=args.ratio)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Add signal handlers
    signals = (signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(
            s, 
            lambda s=s: asyncio.create_task(shutdown(s, loop, panel))
        )
    
    try:
        loop.run_until_complete(panel.run())
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nShutdown initiated...")
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("Shutdown complete.")

if __name__ == '__main__':
    main()

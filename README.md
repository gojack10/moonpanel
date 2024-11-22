# Moonpanel

A real-time terminal-based cryptocurrency trade monitor that provides live updates of crypto trading activities.

## Features

- Real-time trade monitoring in your terminal
- Optional price percentage change display (`-p` flag)
- Optional buy/sell ratio display (`-r` flag)
- Clean, terminal-based interface
- Support for multiple cryptocurrencies

## Installation

```bash
pip install moonpanel
```

## Requirements

- Python 3.7 or higher
- Dependencies:
  - websockets
  - termcolor
  - pytz

## Usage

```bash
moonpanel
```
Ctrl+C to exit

## Command Line Arguments

- `-p, --percent`: Display price percentage changes
- `-r, --ratio`: Display buy/sell ratios
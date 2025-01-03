# Crypto Price Analyzer

This repository contains a Python script that retrieves the real-time price of **BTCUSDT** using the Binance API and performs technical analysis by calculating key indicators. The results are saved in an Excel sheet for further analysis. The script also fetches the current Fear and Greed Index value to provide additional market sentiment insights.

## Features

- Fetches real-time BTCUSDT price data using Binance API.
- Calculates:
  - **EMA 12**
  - **EMA 26**
  - **MACD**
  - **EMA 100**
  - **EMA 200**
- Saves all data in an Excel sheet for easy tracking and visualization.
- Retrieves the market's **Fear and Greed Index** value.
- Allows customization of the trading pair (ticker symbol).

## Requirements

- Python 3.7 or higher
- Required libraries: `binance`, `pandas`, `openpyxl`, `requests`
- Replace your **API key** and **API secret** in the script to connect to the Binance API.

Install the required libraries:
```bash
pip install binance pandas openpyxl requests

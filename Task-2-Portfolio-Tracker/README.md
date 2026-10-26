# Investment Portfolio Tracker

## Overview
A Python-based utility that tracks stock investments, calculates portfolio value, and measures profit or loss for each holding.

## Features
- Validates stock symbols using an S&P 500 company dataset.
- Loads sample stock prices from a CSV file.
- Accepts stock tickers, purchase prices, and quantities.
- Calculates total invested amount and current portfolio value.
- Computes profit/loss and percentage returns.
- Exports portfolio results to `portfolio_summary.csv`.

## Technologies Used
- Python
- CSV file handling
- Dictionaries and sets
- File handling with `pathlib`

## Project Files
- `portfolio.py` — Main application.
- `stock_prices.csv` — Sample stock prices.
- `constituents.csv` — Company ticker dataset.
- `portfolio_summary.csv` — Generated portfolio report.

## How to Run
1. Install Python 3.
2. Ensure all three input and program files are in the same folder.
3. Run `portfolio.py`.
4. Enter the ticker, purchase price, and quantity when prompted.
5. Enter `DONE` to calculate and save the portfolio summary.

## Note
The prices included are sample values, not live market prices. The program can validate company symbols from the dataset, but calculations require a corresponding price in `stock_prices.csv`.

import csv
from pathlib import Path

# Get the folder containing this Python file
BASE_DIR = Path(__file__).parent

PRICE_FILE = BASE_DIR / "stock_prices.csv"
COMPANY_FILE = BASE_DIR / "constituents.csv"
SUMMARY_FILE = BASE_DIR / "portfolio_summary.csv"


def load_stock_prices():
    """Load available sample stock prices from CSV."""
    prices = {}

    try:
        with open(PRICE_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("Error: stock_prices.csv is empty.")
                return {}

            reader.fieldnames = [
                name.strip() for name in reader.fieldnames
            ]

            if not {"Symbol", "CurrentPrice"}.issubset(
                reader.fieldnames
            ):
                print(
                    "Error: stock_prices.csv must contain "
                    "Symbol and CurrentPrice columns."
                )
                return {}

            for row in reader:
                symbol = (row.get("Symbol") or "").strip().upper()
                price_text = (row.get("CurrentPrice") or "").strip()

                if not symbol or not price_text:
                    continue

                try:
                    price = float(price_text)
                    if price > 0:
                        prices[symbol] = price
                except ValueError:
                    print(f"Skipping invalid price for {symbol}.")

    except FileNotFoundError:
        print("Error: stock_prices.csv was not found.")

    return prices


def load_valid_symbols():
    """Load valid company symbols from constituents.csv."""
    symbols = set()

    try:
        with open(
            COMPANY_FILE, "r", newline="", encoding="utf-8-sig"
        ) as file:
            reader = csv.DictReader(file)

            if not reader.fieldnames:
                print("Error: constituents.csv is empty.")
                return set()

            reader.fieldnames = [
                name.strip() for name in reader.fieldnames
            ]

            if "Symbol" not in reader.fieldnames:
                print(
                    "Error: constituents.csv must contain "
                    "a Symbol column."
                )
                return set()

            for row in reader:
                symbol = (row.get("Symbol") or "").strip().upper()
                if symbol:
                    symbols.add(symbol)

    except FileNotFoundError:
        print("Error: constituents.csv was not found.")

    return symbols


def collect_portfolio(prices, valid_symbols):
    """Ask the user for stock purchases and validate each ticker."""
    holdings = []

    print("\n--- Enter Your Stock Holdings ---")
    print("Enter DONE as the ticker when you finish.\n")
    print("Tickers with sample prices:", ", ".join(sorted(prices)))

    while True:
        symbol = input("\nEnter stock ticker: ").strip().upper()

        if symbol == "DONE":
            break

        if not symbol:
            print("Please enter a ticker.")
            continue

        if symbol not in valid_symbols:
            print(
                f"{symbol} is not listed in constituents.csv. "
                "Please check the ticker."
            )
            continue

        if symbol not in prices:
            print(
                f"{symbol} is a valid company symbol, but no sample "
                "price is available in stock_prices.csv."
            )
            print(
                "Add its price to stock_prices.csv before tracking it."
            )
            continue

        try:
            purchase_price = float(
                input("Enter purchase price per share: $")
            )
            quantity = int(input("Enter quantity purchased: "))

            if purchase_price <= 0 or quantity <= 0:
                print("Price and quantity must be greater than zero.")
                continue

        except ValueError:
            print("Please enter a valid number for price and quantity.")
            continue

        holdings.append({
            "Symbol": symbol,
            "PurchasePrice": purchase_price,
            "Quantity": quantity,
            "CurrentPrice": prices[symbol]
        })

        print(f"{symbol} added successfully!")

    return holdings


def calculate_portfolio(holdings):
    """Calculate investment value and profit/loss for each holding."""
    total_invested = 0.0
    total_value = 0.0
    results = []

    for holding in holdings:
        invested = holding["PurchasePrice"] * holding["Quantity"]
        current_value = holding["CurrentPrice"] * holding["Quantity"]
        profit_loss = current_value - invested

        if invested > 0:
            return_percent = (profit_loss / invested) * 100
        else:
            return_percent = 0.0

        result = {
            **holding,
            "Invested": invested,
            "MarketValue": current_value,
            "ProfitLoss": profit_loss,
            "ReturnPercent": return_percent
        }

        results.append(result)
        total_invested += invested
        total_value += current_value

    total_profit_loss = total_value - total_invested

    if total_invested > 0:
        overall_return = (
            total_profit_loss / total_invested
        ) * 100
    else:
        overall_return = 0.0

    totals = {
        "TotalInvested": total_invested,
        "TotalValue": total_value,
        "TotalProfitLoss": total_profit_loss,
        "OverallReturn": overall_return
    }

    return results, totals


def display_portfolio(results, totals):
    """Display individual holdings and overall portfolio performance."""
    if not results:
        print("\nNo holdings were entered.")
        return

    print("\n" + "=" * 80)
    print("             INVESTMENT PORTFOLIO SUMMARY")
    print("=" * 80)

    print(
        f"{'Symbol':<10}{'Quantity':>10}{'Buy Price':>13}"
        f"{'Current':>12}{'Invested':>13}{'Value':>12}"
        f"{'P/L':>12}{'Return %':>11}"
    )
    print("-" * 93)

    for item in results:
        print(
            f"{item['Symbol']:<10}"
            f"{item['Quantity']:>10}"
            f"${item['PurchasePrice']:>12.2f}"
            f"${item['CurrentPrice']:>11.2f}"
            f"${item['Invested']:>12.2f}"
            f"${item['MarketValue']:>11.2f}"
            f"${item['ProfitLoss']:>11.2f}"
            f"{item['ReturnPercent']:>10.2f}%"
        )

    print("-" * 93)
    print(f"Total Invested:  ${totals['TotalInvested']:.2f}")
    print(f"Current Value:   ${totals['TotalValue']:.2f}")
    print(f"Total Profit/Loss: ${totals['TotalProfitLoss']:.2f}")
    print(f"Overall Return:  {totals['OverallReturn']:.2f}%")
    print("=" * 80)


def save_summary(results, totals):
    """Save the holdings and overall totals to a CSV file."""
    columns = [
        "Symbol",
        "PurchasePrice",
        "Quantity",
        "CurrentPrice",
        "Invested",
        "MarketValue",
        "ProfitLoss",
        "ReturnPercent"
    ]

    try:
        with open(
            SUMMARY_FILE, "w", newline="", encoding="utf-8"
        ) as file:
            writer = csv.DictWriter(file, fieldnames=columns)
            writer.writeheader()

            for item in results:
                writer.writerow({
                    key: item[key] for key in columns
                })

            # Add a final row containing overall portfolio totals.
            writer.writerow({
                "Symbol": "TOTAL",
                "Invested": round(totals["TotalInvested"], 2),
                "MarketValue": round(totals["TotalValue"], 2),
                "ProfitLoss": round(totals["TotalProfitLoss"], 2),
                "ReturnPercent": round(totals["OverallReturn"], 2)
            })

        print(f"\nPortfolio summary saved to: {SUMMARY_FILE}")

    except OSError as error:
        print(f"Could not save the summary: {error}")


def main():
    print("=" * 45)
    print("   INVESTMENT PORTFOLIO TRACKER")
    print("=" * 45)

    prices = load_stock_prices()
    valid_symbols = load_valid_symbols()

    if not prices:
        print("No usable sample stock prices found. Exiting.")
        return

    if not valid_symbols:
        print("No valid company symbols found. Exiting.")
        return

    print(f"\nLoaded {len(valid_symbols)} company symbols.")
    print(f"Loaded {len(prices)} sample stock prices.")

    holdings = collect_portfolio(prices, valid_symbols)

    if not holdings:
        print("\nNo holdings to calculate. Exiting.")
        return

    results, totals = calculate_portfolio(holdings)
    display_portfolio(results, totals)
    save_summary(results, totals)


if __name__ == "__main__":
    main()

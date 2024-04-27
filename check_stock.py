import csv
import requests
from alphavantage import AlphaVantage

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=QEDE8SI5XV33UWP0'
r = requests.get(url)
data = r.json()


def read_stock_files(first_name: str, last_name: str) -> list[list[str]]:
    file_name = f"files/stocks/{first_name.lower()}_{last_name.lower()}_stocks.csv"
    try:
        with open(file_name, "r") as file_pointer:
            return list(csv.reader(file_pointer))
    except IOError as e:
        print(f"{file_name} does not exist")
        return []
    
    
if __name__ == '__main__':
    stock = read_stock_files("Giap", "Do",) 
    tickers = []

    AV = AlphaVantage()

    rows = list(stock)
    iterator = iter(rows)
    next(iterator)
    for i,row in enumerate(rows):
        if i == 0:
            continue
        if row:
            tickers.append(row[0])

    print(tickers)

    new_prices = []
    for tick in tickers:
        current_price = AV.get_closing_price(tick)
        new_prices.append(current_price)
    
    print(new_prices)

import csv
import requests

url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=QEDE8SI5XV33UWP0'

r = requests.get(url)

data = r.json()

print(data)


with open('stocks.csv', 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    tickers = []
    for line in csv_reader:
        tickers.append(line[0])
    print(tickers)

def valid_ticker(tickers):
    ticker_validated = True
    for ticker in tickers:
        # loop through the api ticker to check if it exists
            if ticker != api_ticker:
                ticker_validated = False
                break


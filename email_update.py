import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import check_stock as cs
from alphavantage import AlphaVantage
import csv



def update_prices(first_name: str, last_name: str, AV: AlphaVantage):
    file_name = f'files/stocks/{first_name.lower()}_{last_name.lower()}_stocks.csv'
    stock = cs.read_stock_files("Giap", "Do",) 
    tickers = []

    rows = list(stock)
    iterator = iter(rows)
    next(iterator)
    for i,row in enumerate(rows):
        if i == 0:
            continue
        if row:
            tickers.append(row[0])

    new_prices = []
    for tick in tickers:
        new_prices.append(AV.get_closing_price(tick, True))
    
    count = len(rows[0]) if rows else 0
    
    # test both cases
    if count < 4:
        data = cs.read_stock_files(first_name,last_name)
    
        data[0].append('Current Price')
        
        for row, new_price in zip(data[1:], new_prices):
            row.append(new_price)
        
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    elif count < 5:
        data = cs.read_stock_files(first_name,last_name)

        for row, new_price in zip(data[1:], new_prices):
            row[-1] = new_price
        
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
    else:
        print('The format of this csv file is incorrect. It should be 3 or 4 columns')

        
if __name__ == '__main__': 
    AV = AlphaVantage()
    update_prices('Giap', 'Do', AV)
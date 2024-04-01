import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import check_stock as cs
from alphavantage import AlphaVantage
import csv

def send_update(stock_ticker, current_price, original_price, user_email):
    message = MIMEMultipart()
    message['From'] = 'your_email@gmail.com'
    message['To'] = user_email
    message['Subject'] = f'Alert: {stock_ticker} dropped by more than 10%'
    body = f"The stock {stock_ticker} dropped by more than 10%.\n" \
           f"Current Price: ${current_price}\n" \
           f"Original: ${original_price}"
    
    message.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')  # You should use an app password here for security reasons

    text = message.as_string()
    server.sendmail('your_email@gmail.com', user_email, text)
    server.quit()

# change the existing csv file with the updated prices

# def update_prices(first_name: str, last_name: str, AV: AlphaVantage):
#     file_name = f'files/stocks/{first_name.lower()}_{last_name.lower()}_stocks.csv'
#     user_data = cs.read_stock_files(first_name,last_name)
#     tickers = []
#     next(user_data)
#     for row in user_data:
#         tickers.append(row[0])
#     new_prices = [AV.get_closing_price(tick) for tick in tickers]
#     first_row = next(user_data)
#     count = len(first_row)
#     if count < 4:
#         existing_data = []
#         existing_data.append(user_data)
#         existing_data[0].append("Current Price")
#         for i, row in enumerate(existing_data[1:], start=1):
#             row.append(new_prices[i - 1])
#         with open(file_name, 'w', newline='') as csv:
#             writer = csv.writer(csv)
#             writer.writerows(existing_data)
#     else:
#         updated_data = []
#         updated_data.append(user_data)
#         header = user_data[0]
#         for row, new_prices in zip(user_data, new_prices):
#             row[header.index('Current Price')] = new_prices
#             updated_data.append(row)
        
#         with open(file_name, 'w', newline='') as csv:
#             writer = csv.writer(csv)
#             writer.writerows(updated_data)

def update_prices(first_name: str, last_name: str, AV: AlphaVantage, date):
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
        new_prices.append(AV.get_closing_price(tick))
    
    count = len(rows[0]) if rows else 0
    
    if count < 4:
        with open(file_name, 'r', newline='') as file:
            reader = csv.reader(file)
            data = list(reader)  # Read the CSV data into a list
    
        data[0].append('Current Price')
        
        # Add the new prices to each row
        for row, new_price in zip(data[1:], new_prices):
            row.append(new_price)
        
        # Write the updated data back to the CSV file
        with open(file_name, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    else:
        for row, new_price in zip(rows, new_prices):
            row[-1] = new_price
    
        # Write the updated data back to the CSV file
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(rows)
        
if __name__ == '__main__': 
    AV = AlphaVantage()
    update_prices('Giap', 'Do', AV)
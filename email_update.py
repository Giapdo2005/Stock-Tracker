import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import check_stock as cs
from alphavantage import AlphaVantage
import csv


def update_prices(first_name: str, last_name: str, AV: AlphaVantage, test: bool=True):
    file_name = f'files/stocks/{first_name.lower()}_{last_name.lower()}_stocks.csv'
    header, *stock = cs.read_stock_files(first_name, last_name)   
    
    if len(header) == 3:
        header.append('Current Price')
    elif len(header) != 4: 
        print("Incorrect header")

    for i,row in enumerate(stock):
        column_count = len(row)

        if column_count == 3:
            row.append(AV.get_closing_price(row[0], test))
            
        elif column_count == 4:
           row[3] = AV.get_closing_price(row[0], test)
            
        else:
            print(f'Row {i+2} has invalid column count: {column_count}')
        
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(stock)

    
#finish send_update function
def send_update(first_name: str, last_name: str, user_email):
    stocks = cs.read_stock_files(first_name, last_name)
    tickers = get_tickers(first_name, last_name)
    init_prices = get_initial_price(first_name, last_name)
    current_prices = get_current_price(first_name)
    
    subject = 'Stock Update'
    body = f'Dear {first_name}, \n\n'\
            'Here is the latest update on your stocks: \n'\
           
    for ticker, init_price, current_price in zip(tickers, init_prices, current_prices):
       body += f'{ticker}: \n' \
                f'Initial Price: ${init_price} \n' \
                f'Current Price: ${current_price}\n\n'

    # Email content
    message = MIMEMultipart()
    message['From'] = 'your_email@gmail.com'
    message['To'] = user_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Email server setup
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')  # You should use an app password here for security reasons

    # Send email
    text = message.as_string()
    server.sendmail('your_email@gmail.com', user_email, text)
    server.quit()
        
if __name__ == '__main__': 
    AV = AlphaVantage()
    update_prices('Giap', 'Do', AV)
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import check_stock as cs
from alphavantage import AlphaVantage
import csv
import time
import schedule 


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

    
def send_update(first_name: str, last_name: str, user_email):
    try:
        _, *stocks = cs.read_stock_files(first_name, last_name)
        
        subject = 'Stock Update'
        body = f'Dear {first_name.title()}, \n\n'\
                'Here is the latest update on your stocks: \n'\
            
        for row in stocks:
            body += f'{row[0]}: \n' \
                    f'Initial Price: {row[2]} \n' \
                    f'Current Price: {row[3]} \n' \
                    
                    
        body += "Your Stock Tracking Team"

        message = MIMEMultipart()
        message['From'] = 'giapdo1901@gmail.com'
        message['To'] = user_email
        message['Subject'] = subject
        message.attach(MIMEText(body, 'plain'))

        # Email server setup
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("giapdo1901@gmail.com", "hxso xque orls aibg")  # You should use an app password here for security reasons

        # Send email
        text = message.as_string()
        server.sendmail('giapdo1901@gmail.com', user_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f'Error: {e}')

def automate_update(first_name, last_name, user_email):
    try:
        print("Updating Stocks....")
        schedule.every().day.at("20:00").do(send_update(first_name, last_name, user_email))

    except Exception as e:
        print(f'Error: {e}')
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__': 
    AV = AlphaVantage()
    update_prices('Giap', 'Do', AV)
    send_update('giap', 'do', 'giapdo1901@gmail.com')

    users = [
        ('giap', 'do', 'giapdo1901@gmail.com')
    ]

    # Schedule updates for each user
    for user in users:
        first_name, last_name, email = user
        automate_update(first_name, last_name, email)

    # Run scheduler loop to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)
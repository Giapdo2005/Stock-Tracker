import json, requests
import check_stock as cs


class AlphaVantage():
    def __init__(self):
        with open("files/config/config.json", 'r') as fp:
            self.config = json.load(fp)
        self.apikey = self.config['AlphaVantageAPIKey']
        self.URL = 'https://www.alphavantage.co/'
        self.my_dict = {}

    def get_closing_price(self,ticker: str, test: bool=False):
        if test:
            return 35.00
        
        if ticker in self.my_dict:
            return self.my_dict[ticker]
        
        URL = f'{self.URL}query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={self.apikey}'
        r = requests.get(URL)
        data = r.json()

        try:
            latest_date = data["Meta Data"]["3. Last Refreshed"]
            closing_price = data["Time Series (Daily)"][latest_date]["4. close"]

            self.my_dict[ticker] = closing_price
            return closing_price
        except Exception as err:
            print(err)
            print(data)
            raise err
        
        
        
if __name__ == "__main__":
    AV = AlphaVantage()
    print(AV.config['AlphaVantageAPIKey'])
    price = AV.get_closing_price("AAPL")
    print(price)


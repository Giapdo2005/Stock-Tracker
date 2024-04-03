import json, requests
import check_stock as cs


class AlphaVantage():
    def __init__(self):
        with open("files/config/config.json", 'r') as fp:
            self.config = json.load(fp)
        self.apikey = self.config['AlphaVantageAPIKey']
        self.URL = 'https://www.alphavantage.co/'
            

    def get_closing_price(self,ticker: str, test: bool=False):

        if test:
            return 35.00
        URL = f'{self.URL}query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={self.apikey}'
        
        r = requests.get(URL)
        data = r.json()
        try:
            latest_date = data["Meta Data"]["3. Last Refreshed"]
            closing_price = data["Time Series (Daily)"][latest_date]["4. close"]
        except Exception as err:
            print(err)
            print(data)
            raise err

        return closing_price
    

if __name__ == "__main__":
    AV = AlphaVantage()
    print(AV.config['AlphaVantageAPIKey'])
    price = AV.get_closing_price("AAPL")
    print(price)


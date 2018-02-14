from pprint import pprint
import os
import pandas as pd
import sys

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

from ticker import Ticker


class Analyst(Ticker):

    def init(self):
        super().__init__()

    def __str__(self):
        return 'Reporting for duty, sir!'

    def cash_available(self):
        self.request = Analyst.get_account_details(self)
        self.list = self.request["response"]["accounts"]["accountsummary"]
        self.filtered_list = [
            item for item in self.list if item["account"] == self.account][0]
        self.cash = self.filtered_list["accountbalance"]["money"]["total"]
        self.cash = float(self.cash)  # cast as float
        return self.cash

    def dataframe(self):
        self.headers = [field for field in self.quote()['response']['quotes']['quote'][0].keys()]
        self.headers = self.headers.append('nan')
        df = pd.read_csv("C:\\Users\\nicho\\Desktop\\stock-trading\\stock_trader\\2018-01-22 ticker.csv", header=self.headers)

# t = Ticker()
# current = t.quote()['response']['quotes']['quote']

# fromavg = list()
# for stock in current:
#     stock['from-avg'] = (float(stock['ask']) - float(stock['vwap'])) / float(stock['vwap'])
#     fromavg.append(stock['from-avg'])

# fromavg.sort()
# print(fromavg)

# for stock in current:
#     for key, value in stock.items():
#         if value == fromavg[-1]:
#             print(stock['symbol'])
#             x = stock['ask']



# price = float(x)
# print(x, "per share")
# a = Analyst()
# cash = a.cash_available() - 10

# print(f"buy {int(cash/price)} shares")
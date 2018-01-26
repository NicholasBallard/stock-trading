import os
import sys

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

import csv
import datetime
import pprint
import requests
import time
from connector.connection import Connection
from stock_basket import stocks


class Ticker(Connection):

    def __init__(self):
        self.stocks = stocks
        super().__init__()

    def quote(self, symbols=stocks):
        _url = 'https://api.tradeking.com/v1/market/ext/quotes.json'
        payload = {'symbols': symbols}
        request = Ticker.request_to_ally(
            self, url=_url, params=payload)  # post is three times as fast
        # request = requests.post(url=_url, auth=self.oauth, params=payload)

        return request.json()

    def run(self):

        os.makedirs("ticks", exist_ok=True)
        status = True

        while status:

            try:
                quotes = Ticker.quote(self)['response']['quotes']['quote']

                fields = list()
                for key in quotes[0].keys():
                    fields.append(key)

                data = list()
                for quote in quotes:
                    row = list()
                    for value in quote.values():
                        row.append(str(value))
                    data.append(row)

                date = quotes[1]["date"]

                with open(os.path.join(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ticks"), date + " ticker.csv"), "a+", newline='') as file:
                    csv_writer = csv.writer(
                        file, delimiter=',', lineterminator='\n')
                    for line in data:
                        csv_writer.writerow(line)
                file.close()

                time.sleep(3)

                if 'open' in Ticker.market_status():
                    status = True
                else:
                    status = False
                    return

            except Exception:
                continue


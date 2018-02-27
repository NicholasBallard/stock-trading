import os
import sys

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

import csv
import datetime
import pprint
import requests
import time
from connection import Connection
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

        export_path = os.path.abspath(os.path.join(ROOTDIR, '..', '..'))
        os.makedirs(os.path.join(export_path, "ticker_export"), exist_ok=True)
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

                with open(os.path.join(export_path, "ticker_export", date + " ticker.csv"), "a+", newline='') as file:
                    csv_writer = csv.writer(
                        file, delimiter=',', lineterminator='\n')
                    for line in data:
                        csv_writer.writerow(line)
                file.close()

                time.sleep(3)

                if 'open' in Ticker.market_status(self):
                    status = True
                else:
                    status = False
                    return

            except Exception:
                continue

    def stock_performance(self):
        '''
        Write to screen real-time stock changes from open and from the last half hour.
        '''

        quotes = Ticker.quote(self)['response']['quotes']['quote']

        current_tick = list()
        for stock in range(len(quotes)):
            # get opening price
            _open = float(quotes[stock]["opn"])
            # get latest price
            _last_price = float(quotes[stock]["bid"])
            # determine percentage change from open
            chg_from_open = (_last_price - _open) / _open
            # make a rounded percent
            chg_from_open = round((chg_from_open * 100), 2)
            # append features to a list
            stock = list([quotes[stock]["bid_time"], str(
                chg_from_open), quotes[stock]["name"]])
            # add stock features list to current_tick list
            current_tick.append(stock)

        # sort list by nested list index i.e. list[list][2]
        current_tick = sorted(current_tick, key=lambda x: float(x[1]))
        for stock in current_tick:
            for item in stock:
                print(item.ljust(8), end='\t')
            print()
        print('-'*50)

        return

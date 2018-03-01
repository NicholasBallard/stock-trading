import csv
import os
import sys
import time
import xml.etree.ElementTree as et
from collections import OrderedDict
from datetime import datetime
from pprint import pprint
from xml.etree.ElementTree import Element, SubElement, dump

import pandas as pd
import requests
from bs4 import BeautifulSoup
from requests_oauthlib import OAuth1

from ally_account_info import *
from app_trading.fixml_dictionaries import order_types, side_dict
from stock_basket import stocks

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)


class Connection(object):

    def __init__(self):

        self.account = account  # from local file
        self.ckey = consumer_key
        self.csec = consumer_secret
        self.akey = access_token
        self.asec = access_secret
        self.oauth = OAuth1(self.ckey, self.csec, self.akey,
                            self.asec, signature_type='auth_header')

    def request_to_ally(self, url, **params):
        self.request = requests.get(url, auth=self.oauth, **params)

        return self.request

    def market_status(self):
        _url = 'https://api.tradeking.com/v1/market/clock.json'
        request = Connection.request_to_ally(self, url=_url)
        market_status = request.json()["response"]["message"]

        return f"It is {str(datetime.now()).split('.')[0]}.\n{market_status}."

    def get_account_values(self):
        _url = 'https://api.tradeking.com/v1/accounts/balances.json'
        request = Connection.request_to_ally(self, _url)

        return request.json()

    # For the Analyst to work with.
    def get_account_details(self):
        _url = 'https://api.tradeking.com/v1/accounts.json'
        request = Connection.request_to_ally(self, _url)

        return request.json()

    def balance(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/balances.json"
        request = Connection.request_to_ally(self, _url)

        return request.json()

    def holdings(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/holdings.xml"
        request = Connection.request_to_ally(self, _url)
        soup = BeautifulSoup(request.text, "xml")

        return soup

    def history(self, range):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/history.xml"
        params = {'range': range}
        request = Connection.request_to_ally(self, url=_url, params=params)
        soup = BeautifulSoup(request.text, "xml")

        return soup


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

        try:

            quotes = Ticker.quote(self)['response']['quotes']['quote']

            current_tick = list()
            for stock in range(len(quotes)):
                # get opening price
                _open = float(quotes[stock]["opn"])
                # get latest price
                _last_price = float(quotes[stock]["ask"])
                # get cash available to trade
                a = Analyst()
                # should already be a float with a cushion
                _cash = a.cash_available() - 15
                # determine percentage change from open
                chg_from_open = (_last_price - _open) / _open
                # make a rounded percent
                chg_from_open = round((chg_from_open * 100), 2)
                # number of shares can buy with cash available to trade
                num_shares = int(_cash / _last_price)
                # append features to a list
                stock = list([quotes[stock]["ask_time"], str(
                    format(chg_from_open, '.2f')), num_shares, quotes[stock]["name"]])
                # add stock features list to current_tick list
                current_tick.append(stock)

            # sort list by nested list index i.e. list[list][2]
            current_tick = sorted(current_tick, key=lambda x: float(x[1]))
            for stock in current_tick:
                for item in stock:
                    print(item.ljust(8), end='\t')
                print()
            print('-' * 50)
            print("You've got", "$" + str(_cash), "to trade.")
            print("")

        except ZeroDivisionError:

            print("Markets aren't open yet.")


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
        self.headers = [field for field in self.quote(
        )['response']['quotes']['quote'][0].keys()]
        self.headers = self.headers.append('nan')
        df = pd.read_csv(
            "C:\\Users\\nicho\\Desktop\\stock-trading\\stock_trader\\2018-01-22 ticker.csv", header=self.headers)

        return df


class Secretary(Connection):

    '''Prepare daily summary reports. Performance, cash positions, profit and loss, trade summaries.'''

    def __init__(self, name):
        super().__init__()
        self.name = name

    def __str__(self):
        return "Hiya! I'm the secretary. I tell you how well you did today. :)"

    def summarize_day(self):
        # values: all, today, current_week, current_month, last_month
        transactions = Secretary.history(self, "today").findAll('transaction')
        return transactions


class Portfolio(Connection):

    def __init__(self):
        self.portfolio = dict()
        super().__init__()

    def __str__(self):
        return "I'm a portfolio. You are a portfolio. We are a portfolio together."

    # TODO: position

    # TODO: basis

    # TODO: transaction costs

    # TODO: protection plan (sell/cover)

    # TODO: time to planned divestiture


class TaxMan(Connection):
    def init(self):
        super().__init__()

    def __str__(self):
        return "I'm the Tax Man! Gains... losses... I'm your man!"


class FundManager(Analyst):

    def __init__(self):
        super().__init__()

    def __str__(self):
        return "Ready to trade?\nUse this command:\npy -m trader.py t.trade(self, side, order_type, symbol, quantity, limit_price=0, stop_price=0, trailing_stop_offset='1')"

    def trade(self, side, order_type, symbol, quantity, limit_price=0, stop_price=0, trailing_stop_offset='1'):
        order = {"TmInForce": f'{"7" if order_type == "moc" else "0"}', "Typ": order_types[order_type],
                 "Side": side_dict[side], "Acct": f'{self.account}'}
        if order_type in ['limit', 'stop limit']:
            order["Px"] = str(limit_price)
        if order_type in ['stop', 'stop limit']:
            order["StopPx"] = str(stop_price)
        if order_type in ['trailing stop']:
            order["ExecInst"] = "a"

        instrument = {"SecTyp": "CS", "Sym": f'{symbol}'}
        quantity = {"Qty": f'{quantity}'}
        peginstrument = {"OfstTyp": "1", "PegPxTyp": "1",
                         "OfstVal": f'{str(trailing_stop_offset)}'}

        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
        Element(xml_declaration)
        root = Element(
            "FIXML", {'xmlns': 'http://www.fixprotocol.org/FIXML-5-0-SP2'})
        order = SubElement(root, "Order", order)

        if order_type in ['trailing stop']:
            SubElement(order, "PegInstr", peginstrument)

        SubElement(order, "Instrmt", instrument)
        SubElement(order, "OrdQty", quantity)

        self.body = et.tostring(root, encoding="utf8", method="xml")
        # self.body = BeautifulSoup(self.body, 'xml') # so can print nicely with .prettify()

        print(
            f"You want to {side_dict[side]} {quantity} shares of {symbol} with a {order_type} order.")

        res = str(input("Is this correct? ( y / n ) ... "))

        if res.upper() in ['Y', 'YES']:
            yield self.body
            self.make_order()
        elif res.upper() in ['N', 'NO']:
            return self
        else:
            pass

        return self.body

    def preview_order(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/orders/preview.xml"
        self.request = requests.post(_url, auth=self.oauth, data=self.body)

        return self.request.text

    def make_order(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/orders.xml"

        confirmation = input("Place the trade? ... Type YES to confirm.")

        if confirmation.upper() == 'YES':

            # Make the trade
            self.request = requests.post(_url, auth=self.oauth, data=self.body)

            # Return the body of the response
            return self.request.text

        else:
            print("Trade cancelled.\n")

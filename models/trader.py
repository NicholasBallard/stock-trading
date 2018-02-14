import os
import sys

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

from collections import OrderedDict
from pprint import pprint
from stock_trader.fixml_dictionaries import order_types, side_dict
from xml.etree.ElementTree import Element, SubElement, dump
import requests
import xml.etree.ElementTree as et

# from bs4 import BeautifulSoup

from analyst import Analyst


class FundManager(Analyst):

    def __init__(self, name):
        super().__init__()
        self.name = name

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

        return self.body

    def preview_order(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/orders/preview.xml"
        self.request = requests.post(_url, auth=self.oauth, data=self.body)

        return self.request.text

    def make_order(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/orders.xml"
        self.request = requests.post(_url, auth=self.oauth, data=self.body)

        return self.request.text


# x = f.trade("buy", "trailing stop", "KR", 1, trailing_stop_offset='5')

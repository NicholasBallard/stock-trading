from pprint import pprint
import os
import sys

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

import requests
import xml.etree.ElementTree as et
from xml.etree.ElementTree import Element, SubElement, dump
from analyst.models import Analyst
from fixml_dictionaries import order_types, side_dict

class FundManager(Analyst):

    def __init__(self, name):
        super().__init__()
        self.name = name

    def trade(self, side, order_type, symbol, quantity, limit_price=0, stop_price=0):
        order = {"TmInForce": f'{"7" if order_type == "moc" else "0"}', "Typ": order_types[order_type],
                 "Side": side_dict[side], "Acct": f'{self.account}'}
        if order_type in ['limit', 'stop limit']:
            order["Px"] = str(limit_price)
        if order_type in ['stop', 'stop limit']:
            order["StopPx"] = str(stop_price)
        
        instrument = {"SecTyp": "CS", "Sym": f'{symbol}'}
        quantity = {"Qty": f'{quantity}'}

        xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'
        declaration = Element(xml_declaration)
        root = Element(
            "FIXML", {'xmlns': 'http://www.fixprotocol.org/FIXML-5-0-SP2'})
        order = SubElement(root, "Order", order)
        SubElement(order, "Instrmt", instrument)
        SubElement(order, "OrdQty", quantity)

        self.body = et.tostring(root, encoding="utf8", method="xml")

        return self.body

    def preview_order(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/orders/preview.xml"
        self.request = requests.post(_url, auth=self.oauth, data=self.body)

        return self.request.text

    def make_order(self):
        _url = f"https://api.tradeking.com/v1/accounts/{self.account}/orders.xml"
        self.request = requests.post(_url, auth=self.oauth, data=self.body)

        return self.request.text

f = FundManager("Buyer")
print(f.market_status())
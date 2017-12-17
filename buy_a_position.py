import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, dump
from pprint import pprint
import requests
from requests_oauthlib import OAuth1

url = 'https://api.tradeking.com/v1/'
account = '5HK21103'
symbol = 'T'
quantity = '2'
consumer_key = 'ln60Ov3NFKHQY5PGPgSiTdFB5lof9D1eSY8XkqP6CJM4'
consumer_secret = 'O0XDMY6Z80r8eXzIJdjS5KCgmTwVBXxcH90nuNeiwLc5'
access_token = 'mRDbaA3w85Eh77NwNItxoI7fwz91A7agW3Ei4SP7l4o8'
access_secret = '3yT9Y5ajtnv9nZnN3Hvh0Yw8gPmwe8mpFuFXyg8oFMo4'

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

body = \
f"""<?xml version="1.0" encoding="UTF-8"?><FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="1" Side="1" Acct="{account}"><Instrmt SecTyp="CS" Sym="{symbol}"/><OrdQty Qty="{quantity}"/></Order></FIXML>"""

symbol = "TSLA"
quantity = "2"

params = {
    "time_in_force": "0",
    "trade_type": "1",
    "side": "1",
    "account": account,
    "security_type": "CS",
    "symbol": symbol,
    "quantity": quantity,
}

root = Element("FIXML", {'xmlns': 'http://www.fixprotocol.org/FIXML-5-0-SP2'})
order = SubElement(root, "Order", {"TmInForce": f'{params["time_in_force"]}', "Typ": f'{params  ["trade_type"]}', "Side": f'{params["side"]}', "Acct": f'{params["account"]}'})
SubElement(order, "Instrmt", {"SecTyp": f'{params["security_type"]}', "Sym": f'{params["symbol"]}'})
SubElement(order, "OrdQty", {"Qty": f'{params["quantity"]}'})

# adds the xml declaration above the root
data = ET.tostring(root, encoding='utf8', method='xml')

r = requests.post(url=url+'accounts/'+account+'/orders/preview.json', auth=oauth, data=data)

pprint(r.json())


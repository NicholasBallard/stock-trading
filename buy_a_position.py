import os
from pprint import pprint
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, dump
from requests_oauthlib import OAuth1

url = 'https://api.tradeking.com/v1/'
account = '[ENTER YOURS HERE]'
symbol = 'T' # AT&T symbol
quantity = '2'
consumer_key = '[ENTER YOURS HERE]'
consumer_secret = '[ENTER YOURS HERE]'
access_token = '[ENTER YOURS HERE]'
access_secret = '[ENTER YOURS HERE]'

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

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

r = requests.post(url=url+'accounts/'+account+'/orders.json', auth=oauth, data=data)

'''If you feel like streaming the response to a file'''
# f = open(os.path.join(os.path.dirname((os.path.abspath(__file__))), "output_preview_an_order.txt"), "w+")
# f.write(r)
# f.close()

pprint(r.json())
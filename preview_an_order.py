import os
from pprint import pprint
import requests
from requests_oauthlib import OAuth1

url = 'https://api.tradeking.com/v1/'
account = '[ENTER YOURS HERE]'
symbol = 'T'
quantity = '2'
consumer_key = '[ENTER YOURS HERE]'
consumer_secret = '[ENTER YOURS HERE]'
access_token = '[ENTER YOURS HERE]'
access_secret = '[ENTER YOURS HERE]'

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

body = \
f"""<?xml version="1.0" encoding="UTF-8"?><FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="1" Side="1" Acct="{account}"><Instrmt SecTyp="CS" Sym="{symbol}"/><OrdQty Qty="{quantity}"/></Order></FIXML>"""

r = requests.post(url=url+'accounts/'+account+'/orders/preview.json', auth=oauth, data=body)

'''If you feel like streaming the response to a file'''
# f = open(os.path.join(os.path.dirname((os.path.abspath(__file__))), "output_preview_an_order.txt"), "w+")
# f.write(r)
# f.close()

pprint(r.json())
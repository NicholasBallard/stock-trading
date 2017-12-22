from ally_account_info import *
from stock_basket import stock_basket
from pprint import pprint
import os
import re
import json
import requests
import requests_oauthlib
from requests_oauthlib import OAuth1

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret,signature_type='auth_header')

def full_url(base_url, suffix, response_format):
    full_url = base_url + suffix + response_format
    return full_url

# Making stock_basket a set ensures no duplicates.
def stocks(stock_basket):
    stocks = ''
    stocks += ','.join([x for x in stock_basket.split()])
    return stocks

def write_output_to_file(content):
    path, name = os.path.split(__file__)
    name = re.sub('.py', '', name)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 
        "output_"+name+".txt"), "w+") as file:
        json.dump(content.json(), file, indent=4)
    file.close()

url = full_url(url, 'market/ext/quotes', '.json')
stock_basket = stocks(stock_basket)

# Query Parameters https://www.ally.com/api/invest/documentation/market-ext-quotes-get-post/
# symbols | a single symbol or list of comma-delimited symbols (required)
# fids    | a comma-delimited list of data fields (i.e. fids=ask,bid,vol). The fids parameter should be
#           used when a customized list of fields is desired. By default, all
#           applicable data fields are returned.

payload = {'symbols': stock_basket,}

# Can use GET or POST, POST is recommended for larger lists of stocks
data = requests.post(url=url, auth=oauth, params= payload)

write_output_to_file(data)
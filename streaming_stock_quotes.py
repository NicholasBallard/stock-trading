'''
from pprint import pprint
import requests
from requests_oauthlib import OAuth1
from ally_account_info import *

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

base_url = 'https://stream.tradeking.com/v1/market/quotes.json'

payload = {'symbols': 'KR'}

s = requests.Session()
s.auth = oauth
r = s.get(base_url, params=payload, stream=True)

for line in r.iter_lines():
    print("Line: ", line)

with requests.Session() as s:
    s.get(base_url, params=payload)

'''
import logging
from requests import Request, Session
from requests_oauthlib import OAuth1
from ally_account_info import *
from stock_basket import stock_basket

logging.basicConfig(filename='logs\\log_file_'+str(__file__.split('\\')[-1].split('.')[0])+'.csv', level=logging.DEBUG, format=' %(asctime)s - %(levelname)s - %(message)s')

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

base_url = 'https://stream.tradeking.com/v1/market/quotes.json'

s = Session()

def stream(symbols):
    logging.debug(f'Start of streaming symbols {symbols}')
    payload = {'symbols': ','.join(symbols.split())}
    headers = {'connection': 'keep-alive', 'content-type': 'application/json', 
        'transfer-encoding': 'chunked'}
    req = Request('GET', base_url,
                #   headers=headers,
                  params=payload,
                  auth=oauth)

    prepped = s.prepare_request(req)

    resp = s.send(prepped, stream=True)

    # with s.send(prepped, stream=True) as req:

    for line in resp.iter_lines():
        if line:
            logging.debug(f'line is {line}, response content is {resp.content}')
            yield line
    
    logging.debug(f'End of streaming symbols {symbols}')

def read_stream():
    for line in stream('KR'):
        print(line)

read_stream()

s.close()
#! python3

import os
import requests
from pprint import pprint
from abc import ABCMeta, abstractmethod
from requests_oauthlib import OAuth1
from stock_basket import stock_basket


def get_env_variable(var_name):
    ''' Get the environment variable or return an exception. '''
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the {} environment variable.".format(var_name)
        raise KeyError(error_msg)

''' Import credentials from environment variables. '''
ACCOUNT = get_env_variable('ACCOUNT')
CONSUMER_KEY = get_env_variable('CONSUMER_KEY')
CONSUMER_SECRET = get_env_variable('CONSUMER_SECRET')
ACCESS_TOKEN = get_env_variable('ACCESS_TOKEN')
ACCESS_SECRET = get_env_variable('ACCESS_SECRET')
BASE_URL = 'https://api.tradeking.com/v1/'
FORMAT = '.json'

oauth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
               ACCESS_SECRET, signature_type='auth_header')

class Connection(object):
    ''' A Connection object with Ally Invest API. '''

    __metaclass__ = ABCMeta
        
    @abstractmethod
    def connection_type():
        '''Return a string representing the type of connection this is.'''
        pass

    def run(self, **kwargs):
        try:
            r = requests.post(url=self.url, auth=oauth, **kwargs)
            return r.status_code, r.header, r.json()
        except Exception as e:
            return


class Market(Connection):
    '''Market data from the Ally Invest API.'''

    def connection_type(self):
        '''Return a string representing the type of connection this is.'''
        return 'market data'

    def stocks(self, stock_basket):
        stocks = ''
        stocks += ','.join([x for x in stock_basket.split()])
        return stocks
    
    SUFFIX = 'market/ext/quotes'
    stock_basket = stocks(stock_basket)
    fields = 'name,symbol,bid,bid_time,bidsz,bidtick,ask,ask_time,asksz,beta,vl'
    payload = {'symbols': stock_basket, 'fids': fields}
    url = BASE_URL + SUFFIX + FORMAT


class PreviewOrder(Connection):
    ''' Preview Order from a POST to the Ally Invest API. '''
    
    SUFFIX = '/orders/preview'
    url = BASE_URL + 'accounts/' + ACCOUNT + SUFFIX + FORMAT
    symbol = 'T'
    quantity = 2
    body = \
    f"""<?xml version="1.0" encoding="UTF-8"?><FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="1" Side="1" Acct="{ACCOUNT}"><Instrmt SecTyp="CS" Sym="{symbol}"/><OrdQty Qty="{quantity}"/></Order></FIXML>"""
    
    def connection_type(self):
        ''' Return a string representing the type of connection this is. '''
        return 'preview order'

run = PreviewOrder()
run = run.run(data=run.body)
print(run)
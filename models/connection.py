import sys
import os

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

from bs4 import BeautifulSoup
from datetime import datetime
from pprint import pprint
from requests_oauthlib import OAuth1
import requests

from ally_account_info import *


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

c = Connection()

print(c.account)
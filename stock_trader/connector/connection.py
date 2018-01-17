import sys
import os

ROOTDIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOTDIR)

from datetime import datetime
from pprint import pprint
import requests
from requests_oauthlib import OAuth1
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

    def request_to_ally(self, url):
        self.request = requests.get(url, auth=self.oauth)

        return self.request

    def market_status(self):
        _url = 'https://api.tradeking.com/v1/market/clock.json'
        self.request = Connection.request_to_ally(self, url=_url)
        _market_status = self.request.json()["response"]["message"]

        return f"It is {str(datetime.now()).split('.')[0]}.\n{_market_status}."

    def get_account_values(self):
        _url = 'https://api.tradeking.com/v1/accounts/balances.json'
        self.request = Connection.request_to_ally(self, _url)

        return self.request.json()

    # For the Analyst to work with.
    def get_account_details(self):
        _url = 'https://api.tradeking.com/v1/accounts.json'
        self.request = Connection.request_to_ally(self, _url)

        return self.request.json()


c = Connection()
pprint(c.get_account_details())

from __future__ import absolute_import
import requests
from requests_oauthlib import OAuth1

url = 'https://api.tradeking.com/v1/'
account = '5HK21103'
consumer_key = 'ln60Ov3NFKHQY5PGPgSiTdFB5lof9D1eSY8XkqP6CJM4'
consumer_secret = 'O0XDMY6Z80r8eXzIJdjS5KCgmTwVBXxcH90nuNeiwLc5'
access_token = 'mRDbaA3w85Eh77NwNItxoI7fwz91A7agW3Ei4SP7l4o8'
access_secret = '3yT9Y5ajtnv9nZnN3Hvh0Yw8gPmwe8mpFuFXyg8oFMo4'

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

r = requests.get(url=url+'accounts/'+account+'/balances.json', auth=oauth)

print(r.json())
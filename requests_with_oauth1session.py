# requests_with_oauth1session.py

from pprint import pprint
import requests
import requests_oauthlib
from requests_oauthlib import OAuth1Session

url = 'https://api.tradeking.com/v1/'
account = '5HK21103'
consumer_key = 'ln60Ov3NFKHQY5PGPgSiTdFB5lof9D1eSY8XkqP6CJM4'
consumer_secret = 'O0XDMY6Z80r8eXzIJdjS5KCgmTwVBXxcH90nuNeiwLc5'
access_token = 'mRDbaA3w85Eh77NwNItxoI7fwz91A7agW3Ei4SP7l4o8'
access_secret = '3yT9Y5ajtnv9nZnN3Hvh0Yw8gPmwe8mpFuFXyg8oFMo4'

oauth = OAuth1Session(
                    consumer_key,
                    consumer_secret,
                    access_token,
                    access_secret,
)

# by default requests_oauthlib signs the request
# in the header with HMAC-SHA1
r = oauth.get(url+'accounts/'+account+'/balances.json')

pprint(r.text)

# f = open("output_file.txt", "w+")
# pprint(r.text, stream=f)
# f.close()
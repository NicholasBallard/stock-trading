import json
import requests
from io import StringIO
from requests_oauthlib import OAuth1
from ally_account_info import *

f = open("output_pulling_in_market_data.txt", "r")

# s = StringIO(f)

s = json.load(f)

# print(json.dumps(s, indent=4))

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

url = 'https://stream.tradeking.com/v1/market/quotes.json?symbols=KR'

s = requests.session()

# chunked encoded responses
# http://docs.python-requests.org/en/master/user/advanced/#body-content-workflow
with s.get(url, auth=oauth, stream=True, timeout=5) as r:
    for l in r.iter_content(chunk_size=1024):
        print(l)
r.close()
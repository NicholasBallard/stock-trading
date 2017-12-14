# Got a lot of what I needed from the author of the module in the wiki example below:
# https://github.com/joestump/python-oauth2/wiki/Signing-A-Request

import time
import pprint
import oauth2 as oauth

# set the API endpoint
url = 'https://api.tradeking.com/v1/'

# Set the base oauth_* parameters along with any other parameters required for the API call.
params = {
    'oauth_version': "1.0",
    'oauth_nonce': oauth.generate_nonce(), # a nonce is a random number
    'oauth_timestamp': str(int(time.time())), # Ally will time invalidate the request if it times out
    'account': '5HK21103',
}

consumer_key = 'ln60Ov3NFKHQY5PGPgSiTdFB5lof9D1eSY8XkqP6CJM4'
consumer_secret = 'O0XDMY6Z80r8eXzIJdjS5KCgmTwVBXxcH90nuNeiwLc5'
access_token = 'mRDbaA3w85Eh77NwNItxoI7fwz91A7agW3Ei4SP7l4o8'
access_secret = '3yT9Y5ajtnv9nZnN3Hvh0Yw8gPmwe8mpFuFXyg8oFMo4'

token = oauth.Token(key=access_token, secret=access_secret)
consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

# Set our token/key parameters
params['oauth_token'] = token.key
params['oauth_consumer_key'] = consumer.key

# Create our request. Change method, etc., accordingly.
request = oauth.Request(method="GET", url=url, parameters=params)

# sign the request
signature_method = oauth.SignatureMethod_HMAC_SHA1()
request.sign_request(signature_method, consumer, token)

# success!

# Create our client.
client = oauth.Client(consumer, token)

# The OAuth Client request works just like httplib2 for the most part.
resp, content = client.request(url+'accounts/5HK21103/balances.json', "GET")

pprint.pprint(resp)
pprint.pprint(content)
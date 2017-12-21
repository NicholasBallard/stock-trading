from pprint import pprint
import requests
from requests_oauthlib import OAuth1
from ally_account_info import * # Python file with the confident information, add to .gitignore

url = 'https://api.tradeking.com/v1/'
account = account
consumer_key = consumer_key
consumer_secret = consumer_secret
access_token = access_token
access_secret = access_secret

oauth = OAuth1(consumer_key, consumer_secret, access_token, access_secret, signature_type='auth_header')

r = requests.get(url=url+'accounts/'+account+'/history.json', params={'range': 'today'}, auth=oauth)

# f = open(os.path.join(os.path.dirname((os.path.abspath(__file__))), "output_order_history.txt"), "w+")
# f.write(r)
# f.close()

pprint(r.json())
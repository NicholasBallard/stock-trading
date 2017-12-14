# make the oauth api work

from __future__ import absolute_import
import oauth2 as oauth

# create your consumer with the proper key/secret
# consumer = oauth.Consumer(key='your-secret-key',
#     secret='your-consumer-secret')

# request token URL
# request_token_url = "http://api.twitter.com/oauth/request_token"

# create our client
client = oauth.Client(consumer)

# the OAuth Client request works just like httplib2 for the most part
response, content = client.request(request_token_url, "GET")
print(response)
print(content)
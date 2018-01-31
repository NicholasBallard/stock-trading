from requests_oauthlib import OAuth1
from stock_basket import stock_basket


class MarketDataStream(object):

    @staticmethod
    def get_env_variable(var_name):
        '''Get the environment variable or return an exception.'''
        try:
            return os.environ[var_name]
        except KeyError:
            error_msg = "Set the {} environment variable.".format(var_name)
            raise KeyError(error_msg)

    ACCOUNT = get_env_variable('ACCOUNT')
    CONSUMER_KEY = get_env_variable('CONSUMER_KEY')
    CONSUMER_SECRET = get_env_variable('CONSUMER_SECRET')
    ACCESS_TOKEN = get_env_variable('ACCESS_TOKEN')
    ACCESS_SECRET = get_env_variable('ACCESS_SECRET')

    def __init__(self, ):
        '''Return a MarketDataStream object whose '''

    '''Import credentials from environment variables'''

    URL = 'https://api.tradeking.com/v1/market/ext/quotes.json'

    oauth = OAuth1(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN,
                   ACCESS_SECRET, signature_type='auth_header')

    def stocks(self, stock_basket):
        stocks = ''
        stocks += ','.join([x for x in stock_basket.split()])
        return stocks

    stock_basket = stocks(stock_basket)

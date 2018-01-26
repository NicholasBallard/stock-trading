import unittest
from connector.connection import Connection


class ConnectionTestCase(unittest.TestCase):

    def setUp(self):
        self.conn = Connection()


class DefaultConnectionTestCase(ConnectionTestCase):

    def test_getting_the_api_keys(self):
        self.assertTrue(len(self.conn.account) ==
                        8 and isinstance(self.conn.account, str))
        self.assertTrue(len(self.conn.ckey) >
                        10 and isinstance(self.conn.ckey, str))
        self.assertTrue(len(self.conn.csec) >
                        10 and isinstance(self.conn.csec, str))
        self.assertTrue(len(self.conn.akey) >
                        10 and isinstance(self.conn.akey, str))
        self.assertTrue(len(self.conn.asec) >
                        10 and isinstance(self.conn.asec, str))

    # Redundant but helps isolate network issues
    def test_connect_to_ally_invest_servers(self):
        r = self.conn.request_to_ally(
            'https://api.tradeking.com/v1/utility/status.xml')
        self.assertEqual(r.status_code, 200)

    def test_access_trading_account(self):
        r = self.conn.request_to_ally(
            'https://api.tradeking.com/v1/accounts/' + self.conn.account + '.xml')
        self.assertEqual(r.status_code, 200)

    def test_request_with_body(self):
        pass

    def test_market_open_status(self):
        # Testing if Connection method fetches the market status.
        self.shortDescription()

        r = self.conn.request_to_ally(
            'https://api.tradeking.com/v1/market/clock/this_will_fail.json')
        self.assertEqual(r.status_code, 404)

        r = self.conn.market_status()
        self.assertTrue("Market" or "After" in r)

    def test_get_my_accounts(self):
        r = self.conn.get_account_values()
        number_of_accounts = len(r["response"]["accountbalance"])
        self.assertEqual(number_of_accounts, 2)  # I have 2 accounts

    def test_get_account_details(self):
        r = self.conn.get_account_details()
        response_message = r["response"]["error"]
        self.assertEqual(response_message, "Success")
    
    def test_account_specific_balance(self):
        r = self.conn.balance()
        response_message = r["response"]["error"]
        self.assertEqual(response_message, "Success")

    def test_account_specific_holdings(self):
        r = self.conn.holdings()
        self.assertTrue("Success" in r.error.text)

    def test_account_specific_history(self):
        r = self.conn.history("all")
        self.assertTrue("Success" in r.error.text)

if __name__ == '__main__':
    unittest.main()

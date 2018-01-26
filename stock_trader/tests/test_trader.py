import unittest
import requests
from trader.models import FundManager


class SimpleHedgeFundManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = FundManager('Mr. Hedge')


class DefaultHedgeFundManagerTestCase(SimpleHedgeFundManagerTestCase):

    def test_instantiation(self):
        self.assertEqual(self.manager.name, 'Mr. Hedge',
                         'Fund Manager class did not instantiate.')

    def test_preview_order_request(self):
        r = requests.post(f"https://api.tradeking.com/v1/accounts/{self.manager.account}/orders/preview.xml",
                          auth=self.manager.oauth, data=self.manager.trade("buy", "market", "TSLA", 1))
        self.assertIn("principal", r.text,
                      "Call to preview order didn't return right. Check parameters and method.")
        self.assertEqual(r.status_code, requests.codes.ok,
                         "Did not return a 200 code.")

    def test_real_order_call(self):
        trade = self.manager.trade("sell", "market", "F", 0)
        r = requests.post(
            f"https://api.tradeking.com/v1/accounts/{self.manager.account}/orders.xml", auth=self.manager.oauth, data=trade)
        self.assertIn("The quantity is not valid", r.text) # 0 shares invalid
        self.assertEqual(500, r.status_code)

    def test_buy_market_dayorder_fixml(self):
        body = self.manager.trade("buy", "market", "GM", 70)
        self.assertIn("TmInForce=\"0\"", str(body))
        self.assertIn("Sym=\"GM\"", str(body))
        self.assertIn("Qty=\"70\"", str(body))
        self.assertIn("SecTyp=\"CS\"", str(body))
        self.assertIn("Typ=\"1\"", str(body))  # 1 for market
        self.assertIn("Side=\"1\"", str(body))  # 1 for buy

# if __name__ == '__main__':
#     unittest.main()

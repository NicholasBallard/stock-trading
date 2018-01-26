import unittest
from ticker.models import Ticker


class TickerTestCase(unittest.TestCase):

    def setUp(self):
        self.tick = Ticker()


class DefaultTickerTestCase(TickerTestCase):

    def test_ticker_imports_stock_basket(self):
        self.assertTrue(len(self.tick.stocks) > 0,
                        "Ticker class is not importing stock basket.")

    def test_get_stock_quotes_for_whole_basket(self):
        r = self.tick.quote()
        self.assertEqual(self.tick.stocks.count(",") + 1,
                         r.count("asksz") * .5)  # while xml

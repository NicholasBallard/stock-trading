import unittest
from stock_trader.models.portfolio import Portfolio

class PortfolioTestCase(unittest.TestCase):

    def setup(self):
        self.portfolio = Portfolio()

class DefaultPortfolioTestCase(PortfolioTestCase):
    pass
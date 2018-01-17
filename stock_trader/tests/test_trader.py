import unittest
from trader.models import FundManager

class SimpleHedgeFundManagerTestCase(unittest.TestCase):

    def setUp(self):
        self.manager = FundManager('Mr. Hedge')

class DefaultHedgeFundManagerTestCase(SimpleHedgeFundManagerTestCase):
    
    def test_instantiation(self):
        self.assertEqual(self.manager.name, 'Mr. Hedge', 'Fund Manager class did not instantiate.')
    
    

if __name__ == '__main__':
    unittest.main()
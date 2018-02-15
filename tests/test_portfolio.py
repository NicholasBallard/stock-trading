import unittest
from models.por import Portfolio


class PortfolioTestCase(unittest.TestCase):

    def setup(self):
        self.p = Portfolio()


class DefaultPortfolioTestCase(PortfolioTestCase):

    def test_portfolio_inherits_from_connection(self):
        self.assertEqual(self.p.account, '5HK21103')


"""

Arrange: This is the first step of a unit test application. Here we will arrange the test, in other words we will do the necessary setup of the test. For example, to perform the test we need to create an object of the targeted class, if necessary, then we need to create mock objects and other variable initialization, something like this.

Act: This is the middle step of a unit step application. In this step we will execute the test. In other words we will do the actual unit testing and the result will be obtained from the test application. Basically we will call the targeted function in this step using the object that we created in the previous step.

Assert: This is the last step of a unit test application. In this step we will check and verify the returned result with expected results.

"""

# TODO: Grab the day's position. Add to a dictionary.

# TODO:

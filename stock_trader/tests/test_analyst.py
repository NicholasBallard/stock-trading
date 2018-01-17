from json import loads
import unittest
from analyst.models import Analyst
from connector.connection import Connection


class AnalystTestCase(unittest.TestCase):

    def setUp(self):
        self.analyst = Analyst()
        self.conn = Connection()


class DefaultAnalystTestCase(AnalystTestCase):

    def test_instantiation(self):
        self.assertEqual(str(self.analyst), 'Reporting for duty, sir!',
                         'Analyst manager string method did not instantiate.')

    def test_reading_account_information(self):
        r = self.conn.get_account_details()
        self.assertTrue(isinstance(r, dict))  # r.json() returns dict

    def test_calculate_total_securities_to_cash_ratio(self):
        self.fail()

if __name__ == '__main__':
    unittest.main()

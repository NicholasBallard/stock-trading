import unittest
from analyst.models import Analyst


class AnalystTestCase(unittest.TestCase):

    def setUp(self):
        self.analyst = Analyst()


class DefaultAnalystTestCase(AnalystTestCase):

    def test_instantiation(self):
        self.assertEqual(str(self.analyst), 'Reporting for duty, sir!',
                         'Analyst manager string method did not instantiate.')

    def test_reading_account_information(self):
        r = self.analyst.get_account_details()
        self.assertTrue(isinstance(r, dict))  # r.json() returns dict

    def test_calculate_total_securities_to_cash_ratio(self):
        r = self.analyst.cash_available()
        self.assertTrue(isinstance(r, (int, float)))

    def test_loads_pandas_dataframe_from_latest_ticker(self):
        df = self.analyst.dataframe()
        self.assertTrue(type())
        

if __name__ == '__main__':
    unittest.main()

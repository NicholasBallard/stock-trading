import unittest
from app_trading.models.secretary import Secretary

class SecretaryTestCase(unittest.TestCase):

    def setup(self):
        self.sec = Secretary("Vicki")

class DefaultSecretaryTestCase(SecretaryTestCase):

    def test_secretary_instantiation(self):
        self.assertTrue(self.sec.name == "Vicki")
        # self.assertFalse(self.sec, None)

    def test_retreives_day_history(self):
        self.fail()

# if __name__ == '__main__':
#     unittest.main()
import unittest
from bot.config import geocoding_api_key
from bot.geocodeapi import GeocodeApi

class CalculatorTestCase(unittest.TestCase):

    def test_get_cities(self):
        geocode_api = GeocodeApi(geocoding_api_key)
        self.assertEqual(geocode_api.get_cities("Питер")[0]["address"], "Санкт-Петербург")
        self.assertEqual(geocode_api.get_cities("Москва")[0]["address"], "Москва")
        self.assertEqual(geocode_api.get_cities("ЪХЬС34ЦЖФЯ"), [])
        self.assertEqual(geocode_api.get_cities(3), [])
        self.assertEqual(geocode_api.get_cities(True), [])


if __name__ == '__main__':
    unittest.main()
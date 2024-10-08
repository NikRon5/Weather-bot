import sys
import unittest

from marshmallow.fields import Integer

from bot.config import weather_api_key
from bot.weatherapi import WeatherApi


class CalculatorTestCase(unittest.TestCase):

    def test_get_current_weather(self):
        weather_api = WeatherApi(weather_api_key)
        # Saint-Petersburg '30.314494', '59.938676'

        self.assertNotEqual(weather_api.get_current_weather(['30.314494', '59.938676']), {})
        self.assertNotEqual(weather_api.get_current_weather([30, 59]), {})

        self.assertEqual(weather_api.get_current_weather(0), {})
        self.assertEqual(weather_api.get_current_weather(True), {})
        self.assertEqual(weather_api.get_current_weather([True, 59]), {})
        self.assertEqual(weather_api.get_current_weather([str(sys.maxsize), str(sys.maxsize)]), {})


if __name__ == '__main__':
    unittest.main()
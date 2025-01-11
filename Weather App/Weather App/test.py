import unittest
from weather import fetch_weather_data, fetch_forecast_data


class TestWeatherApp(unittest.TestCase):
    passed_tests = 0  # Track the number of passed tests

    def test_valid_city(self):
        result = fetch_weather_data("London")
        self.assertIsNotNone(result)
        self.assertIn("temperature", result)
        TestWeatherApp.passed_tests += 1  # Increment if the test passes

    def test_invalid_city(self):
        result = fetch_weather_data("InvalidCityName")
        self.assertIsNone(result)
        TestWeatherApp.passed_tests += 1  # Increment if the test passes

    def test_forecast_data(self):
        result = fetch_forecast_data("London")
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)
        TestWeatherApp.passed_tests += 1  # Increment if the test passes

    @classmethod
    def tearDownClass(cls):
        total_tests = 3
        score = (cls.passed_tests / total_tests) * 100
        print(f"\nScore: {score:.2f}%")

if __name__ == "__main__":
    unittest.main()

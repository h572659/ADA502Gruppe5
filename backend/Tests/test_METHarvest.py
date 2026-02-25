import unittest
import met_service

class TestMETHarvest(unittest.TestCase):

    def test_hello_world(self):
        self.assertEqual("Hello world", "Hello world")

    def test_fetch_weather(self):
        # Oslo: Lat = 59.9139, Lon = 10.7522
        r = met_service.fetch_weather(59.9139, 10.7522)
        self.assertEqual(200, r.status_code)

if __name__ == "__main__":
    unittest.main()

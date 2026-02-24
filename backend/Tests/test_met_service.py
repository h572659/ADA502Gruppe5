import sys
import pathlib
import unittest
from unittest.mock import patch, Mock

# Ensure backend root is on sys.path so tests can import met_service
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from met_service import fetch_weather
def make_mock_response(status=200, json_data=None, raise_exc=None):
    m = Mock()
    m.status_code = status
    m.json.return_value = json_data if json_data is not None else {"properties": {"timeseries": []}}
    if raise_exc:
        m.raise_for_status.side_effect = raise_exc
    else:
        m.raise_for_status = Mock()
    return m


class TestMetService(unittest.TestCase):

    def test_fetch_weather_returns_json_and_calls_raise(self):
        sample = {"properties": {"timeseries": []}}
        mock_resp = make_mock_response(json_data=sample)

        with patch('met_service.requests.get', return_value=mock_resp) as mock_get:
            resp = fetch_weather(60.388847, 5.323993)
            mock_get.assert_called_once()
            self.assertEqual(resp.json(), sample)
            resp.raise_for_status.assert_called_once()

    def test_met_website_status_is_ok(self):
        """Verify fetch_weather returns a response with status code 200."""
        mock_resp = make_mock_response(status=200)

        with patch('met_service.requests.get', return_value=mock_resp) as mock_get:
            resp = fetch_weather(60.388847, 5.323993)
            mock_get.assert_called_once()
            self.assertEqual(resp.status_code, 200)
            resp.raise_for_status.assert_called_once()


if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import Mock, patch

import requests

from keibascraper.load import BaseLoader, CalendarLoader, DEFAULT_HEADERS


class TestBaseLoaderTransport(unittest.TestCase):
    @patch('keibascraper.load.time.sleep')
    @patch('keibascraper.load.requests.Session')
    def test_result_requests_use_browser_headers_and_db_referer(self, mock_session_class, mock_sleep):
        response = Mock()
        response.text = '<html></html>'
        response.apparent_encoding = 'utf-8'
        response.raise_for_status.return_value = None

        session = Mock()
        session.get.return_value = response
        mock_session_class.return_value = session

        loader = BaseLoader('201206050810')
        content = loader.load_contents('https://db.netkeiba.com/race/201206050810/')

        self.assertEqual(content, '<html></html>')
        session.headers.update.assert_called_once_with(DEFAULT_HEADERS)
        session.get.assert_called_once_with(
            'https://db.netkeiba.com/race/201206050810/',
            headers={'Referer': 'https://db.netkeiba.com/'},
            timeout=20,
        )
        mock_sleep.assert_called_once()

    @patch('keibascraper.load.time.sleep')
    @patch('keibascraper.load.requests.Session')
    def test_request_errors_are_wrapped_without_changing_public_exception(self, mock_session_class, mock_sleep):
        session = Mock()
        session.get.side_effect = requests.HTTPError('403 Client Error')
        mock_session_class.return_value = session

        loader = BaseLoader('201206050810')

        with self.assertRaises(RuntimeError) as context:
            loader.load_contents('https://db.netkeiba.com/race/201206050810/')

        self.assertIn('Failed to load contents from https://db.netkeiba.com/race/201206050810/', str(context.exception))


class TestCalendarLoaderTransport(unittest.TestCase):
    @patch('keibascraper.load.requests.get')
    def test_calendar_requests_use_browser_headers_and_yahoo_referer(self, mock_get):
        response = Mock()
        response.text = '<html></html>'
        response.apparent_encoding = 'utf-8'
        response.raise_for_status.return_value = None
        mock_get.return_value = response

        loader = CalendarLoader(2023, 1)
        content = loader.load_contents('https://sports.yahoo.co.jp/keiba/schedule/monthly?year=2023&month=1')

        self.assertEqual(content, '<html></html>')
        args, kwargs = mock_get.call_args
        self.assertEqual(args[0], 'https://sports.yahoo.co.jp/keiba/schedule/monthly?year=2023&month=1')
        self.assertEqual(kwargs['timeout'], 20)
        self.assertEqual(kwargs['headers']['Referer'], 'https://sports.yahoo.co.jp/')
        for key, value in DEFAULT_HEADERS.items():
            self.assertEqual(kwargs['headers'][key], value)


if __name__ == '__main__':
    unittest.main()

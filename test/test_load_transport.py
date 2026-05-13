import importlib
import unittest
from unittest.mock import Mock, patch

import requests

load_module = importlib.import_module('keibascraper.load')
BaseLoader = load_module.BaseLoader
CalendarLoader = load_module.CalendarLoader
DEFAULT_HEADERS = load_module.DEFAULT_HEADERS


class TestBaseLoaderTransport(unittest.TestCase):
    def test_result_requests_use_browser_headers_and_db_referer(self):
        response = Mock()
        response.text = '<html></html>'
        response.apparent_encoding = 'utf-8'
        response.raise_for_status.return_value = None

        session = Mock()
        session.get.return_value = response

        with patch.object(load_module.time, 'sleep') as mock_sleep, \
             patch.object(load_module, '_create_session', return_value=session) as mock_create_session:
            loader = BaseLoader('201206050810')
            content = loader.load_contents('https://db.netkeiba.com/race/201206050810/')

        self.assertEqual(content, '<html></html>')
        mock_create_session.assert_called_once_with()
        session.get.assert_called_once_with(
            'https://db.netkeiba.com/race/201206050810/',
            headers={'Referer': 'https://db.netkeiba.com/'},
            timeout=20,
        )
        mock_sleep.assert_called_once()

    def test_request_errors_are_wrapped_without_changing_public_exception(self):
        session = Mock()
        session.get.side_effect = requests.HTTPError('403 Client Error')

        with patch.object(load_module.time, 'sleep'), \
             patch.object(load_module, '_create_session', return_value=session):
            loader = BaseLoader('201206050810')

            with self.assertRaises(RuntimeError) as context:
                loader.load_contents('https://db.netkeiba.com/race/201206050810/')

        self.assertIn('Failed to load contents from https://db.netkeiba.com/race/201206050810/', str(context.exception))


class TestCalendarLoaderTransport(unittest.TestCase):
    def test_calendar_requests_use_browser_headers_and_yahoo_referer(self):
        response = Mock()
        response.text = '<html></html>'
        response.apparent_encoding = 'utf-8'
        response.raise_for_status.return_value = None

        with patch.object(load_module.requests, 'get', return_value=response) as mock_get:
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

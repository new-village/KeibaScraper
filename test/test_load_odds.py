# test/test_load_odds.py

import unittest
import keibascraper


class TestOddsLoader(unittest.TestCase):
    """Test OddsLoader with various race IDs."""

    @classmethod
    def setUpClass(cls):
        # Load a valid odds data
        cls.valid_race_id = '202210040602'
        cls.valid_odds_data = keibascraper.load('odds', cls.valid_race_id)

        # Load odds for a race that doesn't exist
        cls.invalid_race_id = '201206050812'
        try:
            cls.invalid_odds_data = keibascraper.load('odds', cls.invalid_race_id)
        except RuntimeError as e:
            cls.invalid_odds_error = e

    def test_valid_odds(self):
        """Test that valid odds data is loaded correctly."""
        odds_list = self.valid_odds_data
        self.assertIsInstance(odds_list, list)
        self.assertGreater(len(odds_list), 0)

    def test_invalid_odds(self):
        """Test that loading odds for an invalid race ID raises an error."""
        # 期待される属性が setUpClass で定義されていることを確認
        self.assertTrue(hasattr(self.__class__, 'invalid_odds_error'), "invalid_odds_error 属性が定義されていません。")
        self.assertIsNotNone(self.__class__.invalid_odds_error)
        self.assertIsInstance(self.__class__.invalid_odds_error, RuntimeError)
        self.assertIn("No valid data found", str(self.__class__.invalid_odds_error))

    def test_odds_content(self):
        """Test content of the odds data for a valid race ID."""
        odds_list = self.valid_odds_data
        expected_odds = {
            'id': '20221004060201',
            'race_id': '202210040602',
            'horse_number': 1,
            'win': 19.4,
            'show_min': 3.9,
            'show_max': 7.4
        }
        self.assertDictEqual(odds_list[0], expected_odds)


if __name__ == '__main__':
    unittest.main()

# test/test_load_horse.py

import unittest
from unittest.mock import patch, Mock
import keibascraper


class TestHorseLoader(unittest.TestCase):
    """Test HorseLoader with various horse IDs."""

    @classmethod
    def setUpClass(cls):
        # Load a valid horse
        cls.valid_horse_id = '1994108729'
        cls.valid_horse_data = keibascraper.load('horse', cls.valid_horse_id)

        # Load a non-existent horse
        cls.invalid_horse_id = '9999102739'
        try:
            cls.invalid_horse_data = keibascraper.load('horse', cls.invalid_horse_id)
        except RuntimeError as e:
            print(e)
            cls.invalid_horse_error = e

    def test_valid_horse_info(self):
        """Test that valid horse info is loaded correctly."""
        horse_info, history_list = self.valid_horse_data
        self.assertIsInstance(horse_info, list)
        self.assertIsInstance(history_list, list)
        self.assertGreater(len(horse_info), 0)
        self.assertGreater(len(history_list), 0)

    def test_invalid_horse_info(self):
        """Test that loading an invalid horse ID raises an error."""
        self.assertTrue(hasattr(self.__class__, 'invalid_horse_error'), "invalid_horse_error 属性が定義されていません。")
        self.assertIsNotNone(self.__class__.invalid_horse_error)
        self.assertIsInstance(self.__class__.invalid_horse_error, RuntimeError)
        self.assertIn("No valid data found", str(self.__class__.invalid_horse_error))

    def test_jra_race_parsing(self):
        """Test parsing of JRA race history for the horse."""
        _, history_list = self.valid_horse_data
        expected_history = {
            'id': '20010505081008',
            'horse_id': '1994108729',
            'race_date': '2001-11-25',
            'place': '東京',
            'round': 5,
            'days': 8,
            'weather': '晴',
            'race_number': 10,
            'race_id': '200105050810',
            'race_name': 'ジャパンC(GI)',
            'head_count': 15,
            'bracket': 5,
            'horse_number': 8,
            'win_odds': 8.1,
            'popularity': 4,
            'rank': 4,
            'jockey_id': '00666',
            'jockey_name': '武豊',
            'burden': 57.0,
            'type': '芝',
            'length': 2400,
            'length_class': 'Long',
            'course': '東京芝2400',
            'condition': '良',
            'rap_time': 144.5,
            'passage_rank': '7-6-8-6',
            'last_3f': 35.8,
            'weight': 428,
            'weight_diff': 0,
            'prize': 3800.0
        }
        self.assertDictEqual(history_list[1], expected_history)

    def test_overseas_race_parsing(self):
        """Test parsing of overseas race history for the horse."""
        self.maxDiff = None
        _, history_list = self.valid_horse_data
        expected_history = {
            'id': '2001G012160509',
            'horse_id': '1994108729',
            'race_date': '2001-12-16',
            'place': '香港',
            'round': None,
            'days': None,
            'weather': None,
            'race_number': 5,
            'race_id': '2001G0121605',
            'race_name': '香港ヴァーズ(GI)',
            'head_count': 14,
            'bracket': None,
            'horse_number': 9,
            'win_odds': None,
            'popularity': 1,
            'rank': 1,
            'jockey_id': '00666',
            'jockey_name': '武豊',
            'burden': 57.1,
            'type': '芝',
            'length': 2400,
            'length_class': 'Long',
            'course': '香港芝2400',
            'condition': '良',
            'rap_time': 147.8,
            'passage_rank': None,
            'last_3f': None,
            'weight': None,
            'weight_diff': None,
            'prize': 0
        }
        self.assertDictEqual(history_list[0], expected_history)


if __name__ == '__main__':
    unittest.main()

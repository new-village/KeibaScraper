# test_load_result.py

import unittest
import keibascraper


class TestResultLoader(unittest.TestCase):
    """Test ResultLoader with various race IDs."""

    @classmethod
    def setUpClass(cls):
        # Load a normal result case including scratches
        cls.valid_race_id = '202006030711'
        cls.valid_result_data = keibascraper.load('result', cls.valid_race_id)

        # Load a race with character encoding issues
        cls.encoding_issue_race_id = '202209020804'
        cls.encoding_issue_data = keibascraper.load('result', cls.encoding_issue_race_id)

        # Load a local race
        cls.local_race_id = '202250030808'
        cls.local_race_data = keibascraper.load('result', cls.local_race_id)

        # Load a race with unexpected time format
        cls.unexpected_time_race_id = '2020C8100404'
        cls.unexpected_time_data = keibascraper.load('result', cls.unexpected_time_race_id)

        # Load a non-existent race
        cls.invalid_race_id = '201206050812'
        try:
            cls.invalid_race_data = keibascraper.load('result', cls.invalid_race_id)
        except RuntimeError as e:
            cls.invalid_race_error = e

    def test_valid_result_info(self):
        """Test that valid race results are loaded correctly."""
        self.assertIsInstance(self.valid_result_data, dict)
        self.assertGreater(len(self.valid_result_data), 0)
        self.assertGreater(len(self.valid_result_data['entry']), 0)

    def test_invalid_result_info(self):
        """Test that loading results for an invalid race ID raises an error."""
        self.assertIsNotNone(self.__class__.invalid_race_error)
        self.assertIsInstance(self.__class__.invalid_race_error, RuntimeError)
        self.assertIn(f"No valid data found", str(self.__class__.invalid_race_error))

    def test_race_info_content(self):
        """Test content of the race info for a valid race ID."""
        race_info = self.valid_result_data.copy()
        entry = race_info.pop('entry')
        expected_race_info = {
            'id': '202006030711',
            'race_number': 11,
            'race_name': '第22回中山グランドジャンプ(JGI)',
            'race_date': '2020-04-18',
            'race_time': '15:40',
            'type': '障害',
            'length': 4250,
            'length_class': 'Extended',
            'handed': None,
            'weather': '雨',
            'condition': '不良',
            'place': '中山',
            'course': '中山障害4250',
            'round': 3,
            'days': 7,
            'head_count': 11,
            'max_prize': 6639.2
        }
        self.assertDictEqual(race_info, expected_race_info)

    def test_result_list_content(self):
        """Test content of the result list for a valid race ID."""
        entry_list = self.valid_result_data['entry']
        expected_result = {
            'id': '20200603071106',
            'race_id': '202006030711',
            'rank': 1,
            'bracket': 6,
            'horse_number': 6,
            'horse_id': '2011101125',
            'horse_name': 'オジュウチョウサン',
            'gender': '牡',
            'age': 9,
            'burden': 63.0,
            'jockey_id': '01059',
            'jockey_name': '石神深一',
            'rap_time': 302.9,
            'diff_time': 0.0,
            'passage_rank': '2-2-1-1',
            'last_3f': 14.3,
            'weight': 510,
            'weight_diff': 0,
            'trainer_id': '01114',
            'trainer_name': '和田正一',
            'prize': 6639.2
        }
        self.assertDictEqual(entry_list[0], expected_result)

    def test_scratch_result(self):
        """Test a result where the horse was scratched (did not run)."""
        entry_list = self.valid_result_data['entry']
        expected_result = {
            'id': '20200603071109',
            'race_id': '202006030711',
            'rank': None,
            'bracket': 7,
            'horse_number': 9,
            'horse_id': '2010101798',
            'horse_name': 'セガールフォンテン',
            'gender': '牡',
            'age': 10,
            'burden': 63.0,
            'jockey_id': '01087',
            'jockey_name': '上野翔',
            'rap_time': None,
            'diff_time': None,
            'passage_rank': '',
            'last_3f': None,
            'weight': 498,
            'weight_diff': -10,
            'trainer_id': '00428',
            'trainer_name': '石毛善彦',
            'prize': 0
        }
        self.assertDictEqual(entry_list[10], expected_result)

    def test_encoding_issue_race(self):
        """Test that race data with encoding issues is parsed correctly."""
        entry = self.encoding_issue_data.pop('entry')
        expected_race_info = {
            'id': '202209020804',
            'race_number': 4,
            'race_name': '3歳未勝利',
            'race_date': '2022-04-17',
            'race_time': '11:20',
            'type': '芝',
            'length': 2200,
            'length_class': 'Long',
            'handed': '右',
            'weather': '晴',
            'condition': '良',
            'place': '阪神',
            'course': '阪神芝2200',
            'round': 2,
            'days': 8,
            'head_count': 18,
            'max_prize': 520.0
        }
        self.assertDictEqual(self.encoding_issue_data, expected_race_info)

    def test_local_race_parsing(self):
        """Test parsing of local race data."""
        entry = self.local_race_data.pop('entry')
        expected_race_info = {
            'id': '202250030808',
            'race_number': 8,
            'race_name': 'C2一',
            'race_date': '2022-03-08',
            'race_time': '16:20',
            'type': 'ダート',
            'length': 1400,
            'length_class': 'Mile',
            'handed': '右',
            'weather': '晴',
            'condition': '良',
            'place': '園田',
            'course': '園田ダート1400',
            'round': 22,
            'days': 4,
            'head_count': 10,
            'max_prize': 60.0
        }
        self.assertDictEqual(self.local_race_data, expected_race_info)

    def test_unexpected_time_format(self):
        """Test parsing of a race with an unexpected time format."""
        entry_list = self.unexpected_time_data['entry']
        # Raptime is normal. Origial Raptime is 2:39:30.
        expected_result = {
            'id': '2020C810040407',
            'race_id': '2020C8100404',
            'rank': 1,
            'bracket': None,
            'horse_number': 7,
            'horse_id': '000a014680',
            'horse_name': 'Sottsass',
            'gender': '牡',
            'age': 4,
            'burden': 59.5,
            'jockey_id': '05473',
            'jockey_name': 'Ｃ．デム',
            'rap_time': 9570.0,
            'diff_time': 0,
            'passage_rank': '',
            'last_3f': None,
            'weight': None,
            'weight_diff': None,
            'trainer_id': 'a02f9',
            'trainer_name': 'ＪＣ．ル',
            'prize': 0.0
        }
        self.assertDictEqual(entry_list[0], expected_result)


if __name__ == '__main__':
    unittest.main()

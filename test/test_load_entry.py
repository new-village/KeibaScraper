# test_load_entry.py

import unittest
import keibascraper


class TestEntryLoader(unittest.TestCase):
    """Test EntryLoader with various race IDs."""

    @classmethod
    def setUpClass(cls):
        # Load a valid race entry
        cls.valid_race_id = '202210040211'
        cls.valid_race, cls.valid_entry = keibascraper.load('entry', cls.valid_race_id)

        # Load a non-existent race entry
        cls.invalid_race_id = '201206050812'
        cls.invalid_race_error = None
        try:
            keibascraper.load('entry', cls.invalid_race_id)
        except RuntimeError as e:
            cls.invalid_race_error = e

    def test_valid_race(self):
        """Test that valid race info and entry list are loaded correctly."""
        self.assertIsInstance(self.valid_race, list)
        self.assertGreater(len(self.valid_race), 0)

        self.assertIsInstance(self.valid_entry, list)
        self.assertGreater(len(self.valid_entry), 0)

    def test_invalid_race(self):
        """Test that loading an invalid race ID raises an error."""
        self.assertIsNotNone(self.__class__.invalid_race_error)
        self.assertIsInstance(self.__class__.invalid_race_error, RuntimeError)
        self.assertIn("No valid data found", str(self.__class__.invalid_race_error))

    def test_race_info_content(self):
        """Test content of the race info for a valid race ID."""
        expected_race = {
            'id': '202210040211',
            'race_number': 11,
            'race_name': '小倉記念',
            'race_date': '2022-08-14',
            'race_time': '15:35',
            'type': '芝',
            'length': 2000,
            'length_class': 'Intermediate',
            'handed': '右',
            'weather': '晴',
            'condition': '良',
            'place': '小倉',
            'course': '小倉芝2000',
            'round': 4,
            'days': 2,
            'head_count': 16,
            'max_prize': 4300.0
        }
        self.assertDictEqual(self.valid_race[0], expected_race)

    def test_entry_list_content(self):
        """Test content of the entry list for a valid race ID."""
        expected_entry = {
            'id': '20221004021102',
            'race_id': '202210040211',
            'bracket': 1,
            'horse_number': 2,
            'horse_id': '2018100927',
            'horse_name': 'マリアエレーナ',
            'gender': '牝',
            'age': 4,
            'burden': 54.0,
            'jockey_id': '01126',
            'jockey_name': '松山',
            'trainer_id': '01101',
            'trainer_name': '吉田',
            'weight': 424,
            'weight_diff': -2
        }
        self.assertDictEqual(self.valid_entry[1], expected_entry)

    def test_scratch_entry(self):
        """Test an entry where the horse was scratched (did not run)."""
        expected_entry = {
            'id': '20221004021108',
            'race_id': '202210040211',
            'bracket': 4,
            'horse_number': 8,
            'horse_id': '2017105106',
            'horse_name': 'プリマヴィスタ',
            'gender': '牡',
            'age': 5,
            'burden': 53.0,
            'jockey_id': '01130',
            'jockey_name': '高倉',
            'trainer_id': '01075',
            'trainer_name': '矢作',
            'weight': None,
            'weight_diff': None
        }
        self.assertDictEqual(self.valid_entry[7], expected_entry)


if __name__ == '__main__':
    unittest.main()

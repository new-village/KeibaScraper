# test_load_entry.py

import os
import unittest
import keibascraper


@unittest.skipUnless(os.getenv('KEIBASCRAPER_LIVE_TESTS'), 'set KEIBASCRAPER_LIVE_TESTS=1 to run live netkeiba tests')
class TestEntryLoader(unittest.TestCase):
    """Test EntryLoader with various race IDs."""

    @classmethod
    def setUpClass(cls):
        # Load a valid race entry
        cls.valid_yyyymm = '202301'
        cls.valid_race_ids = keibascraper.race_list(cls.valid_yyyymm[:4], cls.valid_yyyymm[-2:])

    def test_valid_race_list(self):
        """Test that valid race info is loaded correctly."""
        self.assertIsInstance(self.valid_race_ids, list)
        self.assertEqual(len(self.valid_race_ids), 312)

if __name__ == '__main__':
    unittest.main()

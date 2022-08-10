''' test_parser.py
'''
import unittest

from nkparser import load, parse


class TestNkParser(unittest.TestCase):
    ''' TestNkParser
    '''
    @classmethod
    def setUpClass(cls):
        # Load class
        cls.loader = load.NkLoader()
        cls.parser = parse.NkParser()

    def _load_entry(self, race_id):
        return self.loader.load('ENTRY', race_id)

    def test_entry_normal(self):
        ''' test_entry_normal
        '''
        # Load Arima Kinen page
        text = self._load_entry('201206050810')
        entry = self.parser.parse('ENTRY', text)
        #[(print(e)) for e in entry]
        # Compare result
        self.assertEqual(len(entry), 16)

    def test_entry_nonexistent_id(self):
        ''' test_entry_nonexistent_id
        '''
        # Non-exist pages
        text = self._load_entry('201206050899')
        with self.assertRaises(SystemExit):
            self.parser.parse('ENTRY', text)

    def test_race_normal(self):
        ''' test_race_normal
        '''
        # Load Arima Kinen page
        text = self._load_entry('201206050810')
        race = self.parser.parse('RACE', text)
        # [(print(e)) for e in race]
        # Compare result
        self.assertEqual(len(race), 1)

    def test_race_nonexistent_id(self):
        ''' test_race_nonexistent_id
        '''
        # Load Arima Kinen page
        text = self._load_entry('201206050899')
        with self.assertRaises(SystemExit):
            self.parser.parse('RACE', text)

    def _load_odds(self, race_id):
        return self.loader.load('ODDS', race_id)

    def test_odds_normal(self):
        ''' test_odds_normal
        '''
        # Load Arima Kinen page
        text = self._load_odds('201206050810')
        odds = self.parser.parse('ODDS', text)
        # [(print(o)) for o in odds]
        # Compare result
        self.assertEqual(len(odds), 16)

    def _load_result(self, race_id):
        return self.loader.load('RESULT', race_id)

    def test_result_normal(self):
        ''' test_result_normal
        '''
        # Load Arima Kinen page
        text = self._load_result('201206050810')
        race = self.parser.parse('RESULT', text)
        # [(print(r)) for r in race]
        # Compare result
        self.assertEqual(len(race), 16)

if __name__ == '__main__':
    unittest.main()
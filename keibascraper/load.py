# load.py

import time
import random
import requests

from keibascraper.helper import load_config
from keibascraper.parse import parse_html, parse_json


def load(data_type, entity_id):
    """
    Load data from netkeiba.com based on the specified data type and entity ID.
    """
    loaders = {
        'entry': EntryLoader,
        'odds': OddsLoader,
        'result': ResultLoader,
        'horse': HorseLoader,
    }

    loader_class = loaders.get(data_type)
    if not loader_class:
        raise ValueError(f"Unexpected data type: {data_type}")

    loader = loader_class(entity_id)
    return loader.load()

def race_list(year:int, month:int) -> list:
    """ collect arguments race id. """
    calc = CalendarLoader(year, month)
    return calc.load()

class BaseLoader:
    def __init__(self, entity_id):
        self.entity_id = entity_id

    def create_url(self, base_url):
        return base_url.replace('{ID}', self.entity_id)

    def load_contents(self, url):
        time.sleep(random.uniform(2, 3))
        headers = {
            'User-Agent': (
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/58.0.3029.110 Safari/537.3'
            )
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response.encoding = 'EUC-JP'
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to load contents from {url}") from e

    def parse_with_error_handling(self, parse_funcs):
        results = []
        for parse_func, args in parse_funcs:
            try:
                result = parse_func(*args)
                results.append(result)
            except RuntimeError as e:
                raise RuntimeError(f"Failed to parse data for {self.entity_id}: {e}") from e
        return results


class EntryLoader(BaseLoader):
    def load(self):
        config = load_config('entry')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)

        parse_funcs = [
            (parse_html, ('race', content, self.entity_id)),
            (parse_html, ('entry', content, self.entity_id))
        ]
        race, entry = self.parse_with_error_handling(parse_funcs)

        return race, entry


class OddsLoader(BaseLoader):
    def load(self):
        config = load_config('odds')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)

        parse_funcs = [
            (parse_json, ('odds', content, self.entity_id))
        ]
        odds_data, = self.parse_with_error_handling(parse_funcs)
        return odds_data


class ResultLoader(BaseLoader):
    def load(self):
        config = load_config('result')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)

        parse_funcs = [
            (parse_html, ('race_db', content, self.entity_id)),
            (parse_html, ('result', content, self.entity_id))
        ]
        race, entry = self.parse_with_error_handling(parse_funcs)

        return race, entry


class HorseLoader(BaseLoader):
    def load(self):
        config = load_config('horse')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)

        parse_funcs = [
            (parse_html, ('horse', content, self.entity_id)),
            (parse_html, ('history', content, self.entity_id))
        ]
        horse, history = self.parse_with_error_handling(parse_funcs)

        return horse, history


class CalendarLoader:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    def load(self):
        url = f"https://keiba.yahoo.co.jp/schedule/list/{self.year}/?month={self.month}"
        content = self.load_contents(url)
        race_ids = parse_html('cal', content)
        return self.expand_race_ids(race_ids)

    def load_contents(self, url):
        try:
            response = requests.get(url)
            response.encoding = 'EUC-JP'
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to load contents from {url}") from e
    
    def expand_race_ids(self, input_data):
        race_ids = []
        for item in input_data:
            race_id = item.get('race_id')
            if not race_id:
                print(f"Warning: Item {item} does not contain 'race_id'. Skipping.")
                continue
            
            if len(race_id) == 8:
                base_id = '20' + race_id
                expanded_ids = [f"{base_id}{str(i).zfill(2)}" for i in range(1, 13)]
                race_ids.extend(expanded_ids)
            else:
                print(f"Warning: race_id '{race_id}' has invalid length ({len(race_id)}). Skipping.")
        
        return race_ids

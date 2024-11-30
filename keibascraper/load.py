# load.py

import time
import random
import requests

from keibascraper.helper import load_config
from keibascraper.parse import parse_html, parse_json


def load(data_type, entity_id):
    """
    Load data from netkeiba.com based on the specified data type and entity ID.

    Parameters:
        data_type (str): Type of data to load ('entry', 'odds', 'result', 'horse').
        entity_id (str): Identifier for the data entity (e.g., race ID, horse ID).

    Returns:
        tuple or list: Parsed data corresponding to the data type.

    Raises:
        ValueError: If an unsupported data type is provided.
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
    """ collect arguments race id.
    :param year: target year
    :param month: target month
    """
    calc = CalendarLoader(year, month)
    return calc.exec()

class BaseLoader:
    """
    Base loader class providing common functionality for all loaders.

    Attributes:
        entity_id (str): Identifier for the data entity.
    """

    def __init__(self, entity_id):
        self.entity_id = entity_id

    def create_url(self, base_url):
        """
        Generate the full URL by replacing placeholders with actual entity IDs.

        Parameters:
            base_url (str): Base URL containing placeholders.

        Returns:
            str: URL with placeholders replaced by entity IDs.
        """
        return base_url.replace('{ID}', self.entity_id)

    def load_contents(self, url):
        """
        Fetch content from the given URL while respecting rate limits.

        Parameters:
            url (str): URL to fetch data from.

        Returns:
            str: Response text from the URL.

        Raises:
            RuntimeError: If the request fails due to network issues or invalid URLs.
        """
        # Wait for rate limiting (2-3 seconds)
        time.sleep(random.uniform(2, 3))
        # Set User-Agent header
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
        """
        Parse content using provided parsing functions with error handling.

        Parameters:
            parse_funcs (list): List of tuples containing parse functions and their arguments.

        Returns:
            list: List of parsed data.

        Raises:
            RuntimeError: If parsing fails.
        """
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
        """
        Load entry data including race information and entry list.

        Returns:
            tuple: A tuple containing race info and entry list dictionaries.

        Raises:
            RuntimeError: If no valid data is found.
        """
        config = load_config('entry')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)
        try:
            race_info = parse_html('race', content, self.entity_id)
            entry_list = parse_html('entry', content, self.entity_id)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to load entry data for race ID {self.entity_id}: {e}") from e
        
        parse_funcs = [
            (parse_html, ('race', content, self.entity_id)),
            (parse_html, ('entry', content, self.entity_id))
        ]
        race_info, entry_list = self.parse_with_error_handling(parse_funcs)
        
        # Nesting the data
        race_info = race_info[0]
        race_info['entry'] = entry_list
        return race_info

class OddsLoader(BaseLoader):
    """
    Loader for fetching odds data.
    """

    def load(self):
        """
        Load odds data.

        Returns:
            list: A list of dictionaries containing odds information.

        Raises:
            RuntimeError: If no valid data is found.
        """
        config = load_config('odds')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)
        try:
            odds_data = parse_json('odds', content, self.entity_id)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to load odds data for race ID {self.entity_id}: {e}") from e

        parse_funcs = [
            (parse_json, ('odds', content, self.entity_id))
        ]
        odds_data, = self.parse_with_error_handling(parse_funcs)
        return odds_data


class ResultLoader(BaseLoader):
    """
    Loader for fetching race results.
    """

    def load(self):
        """
        Load race results including race information and result list.

        Returns:
            tuple: A tuple containing race info and result list dictionaries.

        Raises:
            RuntimeError: If no valid data is found.
        """
        config = load_config('result')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)

        try:
            race_info = parse_html('race_db', content, self.entity_id)
            result_list = parse_html('result', content, self.entity_id)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to load result data for race ID {self.entity_id}: {e}") from e

        parse_funcs = [
            (parse_html, ('race_db', content, self.entity_id)),
            (parse_html, ('result', content, self.entity_id))
        ]
        race_info, result_list = self.parse_with_error_handling(parse_funcs)

        # Nesting the data
        race_info = race_info[0]
        race_info['entry'] = result_list
        return race_info


class HorseLoader(BaseLoader):
    """
    Loader for fetching horse data.
    """

    def load(self):
        """
        Load horse data including horse information and history.

        Returns:
            tuple: A tuple containing horse info and history list dictionaries.

        Raises:
            RuntimeError: If no valid data is found.
        """
        config = load_config('horse')
        url = self.create_url(config['property']['url'])
        content = self.load_contents(url)
        try:
            horse_info = parse_html('horse', content, self.entity_id)
            history_list = parse_html('history', content, self.entity_id)
        except RuntimeError as e:
            raise RuntimeError(f"Failed to load horse data for horse ID {self.entity_id}: {e}") from e

        parse_funcs = [
            (parse_html, ('horse', content, self.entity_id)),
            (parse_html, ('history', content, self.entity_id))
        ]
        horse_info, history_list = self.parse_with_error_handling(parse_funcs)

        # Nesting the data
        horse_info = horse_info[0]
        horse_info['entry'] = history_list
        return horse_info


class CalendarLoader:
    """
    Loader for fetching calendar data.

    Attributes:
        year (int): The year for which to load the calendar.
        month (int): The month for which to load the calendar.
    """

    def __init__(self, year, month):
        self.year = year
        self.month = month

    def load(self):
        """
        Load calendar data for the specified year and month.

        Returns:
            list: A list of race IDs extracted from the calendar.
        """
        url = f"https://keiba.yahoo.co.jp/schedule/list/{self.year}/?month={self.month}"
        content = self.load_contents(url)
        race_ids = parse_html('cal', content)
        return race_ids

    def load_contents(self, url):
        """
        Fetch calendar content from the given URL while respecting rate limits.

        Parameters:
            url (str): URL to fetch calendar data from.

        Returns:
            str: Response text from the URL.

        Raises:
            RuntimeError: If the request fails due to network issues or invalid URLs.
        """
        # Wait for rate limiting (2-3 seconds)
        time.sleep(random.uniform(2, 3))
        try:
            response = requests.get(url)
            response.encoding = 'EUC-JP'
            return response.text
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to load contents from {url}") from e

# parse.py

import json
import itertools
import jq
from bs4 import BeautifulSoup, Tag

from keibascraper.helper import *


def parse_html(data_type, text, entity_id=None):
    """
    Parse HTML content based on the configuration for the specified data type.

    Parameters:
        data_type (str): Type of data to parse.
        text (str): HTML content to parse.
        entity_id (str, optional): Identifier for the data entity.

    Returns:
        list or dict: Parsed data as a list or dictionary.
    """
    parser = HTMLParser(data_type, text, entity_id)
    return parser.parse()


def parse_json(data_type, text, entity_id=None):
    """
    Parse JSON content based on the configuration for the specified data type.

    Parameters:
        data_type (str): Type of data to parse.
        text (str): JSON content to parse.
        entity_id (str, optional): Identifier for the data entity.

    Returns:
        list or dict: Parsed data as a list or dictionary.
    """
    parser = JSONParser(data_type, text, entity_id)
    return parser.parse()


class BaseParser:
    """
    Base parser class providing common functionality for HTML and JSON parsers.

    Attributes:
        data_type (str): Type of data to parse.
        text (str): Content to parse.
        entity_id (str, optional): Identifier for the data entity.
        config (dict): Parsing configuration loaded from the config file.
    """

    def __init__(self, data_type, text, entity_id):
        self.data_type = data_type
        self.text = text
        self.entity_id = entity_id
        self.config = load_config(data_type)
        self.columns = self.config.get('columns', [])
        self.selector = self.config['property'].get('selector', '')
        self.validator = self.config['property'].get('validator', '')

    def apply_pre_func(self, col, record):
        """
        Apply pre-processing function to the specified column in the record.

        Parameters:
            col (dict): Column configuration.
            record (dict): Record containing the data.

        Returns:
            Any: Processed value for the column.
        """
        value = record.get(col['col_name'])
        if 'pre_func' in col:
            func_name = col['pre_func']['name']
            args = [record[arg] for arg in col['pre_func']['args']]
            func = globals().get(func_name)
            if not func:
                raise ValueError(f"Function {func_name} is not defined.")
            value = func(*args)
        elif isinstance(value, Tag):
            value = value.get_text(strip=True)
        return value

    def apply_post_func(self, col, record):
        """
        Apply post-processing function to the specified column in the record.

        Parameters:
            col (dict): Column configuration.
            record (dict): Record containing the data.

        Returns:
            Any: Processed value for the column.
        """
        value = record.get(col['col_name'])
        if 'post_func' in col:
            func_name = col['post_func']['name']
            args = [record[arg] for arg in col['post_func']['args']]
            func = globals().get(func_name)
            if not func:
                raise ValueError(f"Function {func_name} is not defined.")
            value = func(*args)
        return value

    def apply_format(self, col, value):
        """
        Apply formatting to the value based on the column configuration.

        Parameters:
            col (dict): Column configuration.
            value (Any): Value to format.

        Returns:
            Any: Formatted value.
        """
        if 'reg' in col and value is not None:
            value = formatter(col['reg'], value, col['var_type'])
        return value

    def add_entity_id(self, col, record):
        """
        Add entity ID to the record if specified in the column configuration.

        Parameters:
            col (dict): Column configuration.
            record (dict): Record containing the data.

        Returns:
            Any: Value with entity ID added if applicable.
        """
        if col.get('index') == 'entity_id':
            return self.entity_id
        else:
            return record.get(col['col_name'])


class HTMLParser(BaseParser):
    """
    Parser for processing HTML content.
    """

    def parse(self):
        """
        Parse the HTML content and extract data based on the configuration.

        Returns:
            list: List of dictionaries containing parsed data.

        Raises:
            RuntimeError: If the data is invalid or not found.
        """
        soup = BeautifulSoup(self.text, 'html.parser')

        # Check for invalid data indicators
        if self.is_invalid_data(soup):
            raise RuntimeError(f"No valid data found for {self.data_type} with ID {self.entity_id}")

        elements = soup.select(self.selector)
        if not elements:
            raise RuntimeError(f"No elements found for selector {self.selector}")

        records = []

        for element in elements:
            record = {}
            for col in self.columns:
                col_name = col['col_name']
                selector = col['selector']
                selected = element.select_one(selector)
                record[col_name] = selected

            # Apply pre-processing, formatting, and post-processing
            for col in self.columns:
                col_name = col['col_name']
                record[col_name] = self.apply_pre_func(col, record)
                record[col_name] = self.apply_format(col, record[col_name])
                record[col_name] = self.add_entity_id(col, record)
                record[col_name] = self.apply_post_func(col, record)

            records.append(record)
        return records

    def is_invalid_data(self, soup):
        """
        Check if the soup indicates invalid or missing data.

        Parameters:
            soup (BeautifulSoup): Parsed HTML content.

        Returns:
            bool: True if data is invalid, False otherwise.
        """
        # Check for a specific error message or missing validator element
        if soup.find(string="該当するデータはありません") or not soup.select_one(self.validator):
            return True
        return False

class JSONParser(BaseParser):
    """
    Parser for processing JSON content.
    """

    def parse(self):
        """
        Parse the JSON content and extract data based on the configuration.

        Returns:
            list: List of dictionaries containing parsed data.

        Raises:
            RuntimeError: If the data is invalid or not found.
        """
        try:
            data = json.loads(self.text)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON content for {self.data_type} with ID {self.entity_id}") from e

        # Check for invalid data indicators
        if self.is_invalid_data(data):
            raise RuntimeError(f"No valid data found for {self.data_type} with ID {self.entity_id}")

        records = []

        # Extract data for each column
        columns_data = []
        for col in self.columns:
            selector = col['selector']
            try:
                jq_program = jq.compile(selector)
                column_data = jq_program.input(data).all()
            except Exception:
                column_data = []
            columns_data.append(column_data)

        # Transpose the data and create records
        for values in itertools.zip_longest(*columns_data):
            record = {}
            for col, value in zip(self.columns, values):
                record[col['col_name']] = value

            # Apply pre-processing, formatting, and post-processing
            for col in self.columns:
                col_name = col['col_name']
                record[col_name] = self.apply_pre_func(col, record)
                record[col_name] = self.apply_format(col, record[col_name])
                record[col_name] = self.add_entity_id(col, record)
                record[col_name] = self.apply_post_func(col, record)

            records.append(record)
        return records

    def is_invalid_data(self, data):
        """
        Check if the JSON data indicates invalid or missing data.

        Parameters:
            data (dict): Parsed JSON content.

        Returns:
            bool: True if data is invalid, False otherwise.
        """
        # Check if 'data' key is missing or if 'error' key is present
        if not data.get('data') or data.get('error'):
            return True
        return False
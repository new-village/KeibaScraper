# helper.py

import json
import os
import re
from datetime import datetime
from bs4 import Tag
from functools import lru_cache


def formatter(pattern, target, var_type):
    """
    Extract and convert a substring from the target string based on a regex pattern.

    Parameters:
        pattern (str): Regular expression pattern to match.
        target (str): String to extract data from.
        var_type (str): Type to convert the extracted data into ('integer', 'real', 'text').

    Returns:
        Any: Extracted and converted value, or None if no match is found or conversion fails.
    """
    # Search for the pattern in the target string
    match = re.search(pattern, target)
    if not match:
        return None  # Return None if no match is found

    # Determine whether to use a capture group or the entire match
    if match.groups():
        value = match.group(1)  # Use the first capture group if available
    else:
        value = match.group(0)  # Use the entire matched string if no capture groups

    # Remove commas for numerical conversions to handle numbers like "1,234"
    if var_type in ['integer', 'real']:
        value = value.replace(',', '')

    try:
        # Convert the extracted value to the specified type
        if var_type == 'integer':
            return int(value)
        elif var_type == 'real':
            return float(value)
        elif var_type == 'text':
            return value
        else:
            # Raise an error if the var_type is not supported
            raise ValueError(f"Unsupported var_type: {var_type}")
    except (ValueError, TypeError):
        # Return None if conversion fails due to invalid data
        return None


def time_to_seconds(time_str):
    """
    Convert a time string into seconds.

    Parameters:
        time_str (str): Time string in the format 'M:S.F' or 'H:M:S.F'.

    Returns:
        float or None: Time in seconds, or None if input is invalid.
    """
    if not time_str:
        return None

    parts = time_str.text.split(':')
    try:
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return str(int(hours) * 3600 + int(minutes) * 60 + float(seconds))
        elif len(parts) == 2:
            minutes, seconds = parts
            return str(int(minutes) * 60 + float(seconds))
        elif len(parts) == 1:
            return parts[0]
        else:
            return None  # Invalid fromat
    except (ValueError, TypeError):
        return None  # failure to transform


def zero_suppress(value):
    """
    Remove leading zeros from a numeric string.

    Parameters:
        value (str): Numeric string possibly with leading zeros.

    Returns:
        str: Numeric string without leading zeros.
    """
    return str(int(value))


def zero_fill(value):
    """
    Replace None with zero.

    Parameters:
        value (Any): Value to check.

    Returns:
        Any: Original value or zero if None.
    """
    return value if value is not None else 0


def get_title(soup: Tag) -> str:
    """ description
    """
    return soup.get("title") if soup is not None else None


def get_url(soup: Tag) -> str:
    """ description
    """
    return soup.get("href") if soup is not None else None


def count_tr(soup: Tag) -> int:
    """ Counting TR elements in the soup for filling head count.
    :param soup: bs4 object includes Table element.
    :return: Int object
    """
    return len(soup.select("tr")) - 1


def create_uid(race_id, horse_number):
    """
    Create a unique identifier by combining race ID and horse number.

    Parameters:
        race_id (str): Race identifier.
        horse_number (int): Horse number.

    Returns:
        str: Unique identifier string.
    """
    return f"{race_id}{str(horse_number).zfill(2)}"


FIRST_RAP_TIME = 0.0


def set_diff_time(rank, rap_time):
    """
    Calculate the time difference from the first-place horse.

    Parameters:
        rank (int): Rank of the horse.
        rap_time (float): Recorded time of the horse.

    Returns:
        float: Time difference from the first-place horse.
    """
    global FIRST_RAP_TIME
    if rank == 1 and rap_time is not None:
        FIRST_RAP_TIME = rap_time
        return 0.0
    elif rap_time is not None:
        return rap_time - FIRST_RAP_TIME
    else:
        return None


def convert_type(type_abbr):
    """
    Convert race type abbreviation to full form.

    Parameters:
        type_abbr (str): Abbreviation of the race type.

    Returns:
        str: Full form of the race type.
    """
    type_dict = {'芝': '芝', 'ダ': 'ダート', '障': '障害'}
    return type_dict.get(type_abbr, type_abbr)


def classify_length(length):
    """
    Classify race length into predefined categories.

    Parameters:
        length (int): Length of the race in meters.

    Returns:
        str: Category of the race length.
    """
    if length < 1400:
        return 'Sprint'
    elif 1400 <= length < 1800:
        return 'Mile'
    elif 1800 <= length < 2200:
        return 'Intermediate'
    elif 2200 <= length < 2800:
        return 'Long'
    else:
        return 'Extended'


def concat(*args):
    """
    Concatenate multiple arguments into a single string.

    Parameters:
        *args: Arguments to concatenate.

    Returns:
        str: Concatenated string.
    """
    return ''.join(map(str, args))


def fmt_date(date_str):
    """
    Format a date string from 'YYYYMMDD' to 'YYYY-MM-DD'.

    Parameters:
        date_str (str): Date string in 'YYYYMMDD' format.

    Returns:
        str: Formatted date string in 'YYYY-MM-DD' format.
    """
    return datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')


@lru_cache(maxsize=None)
def load_config(data_type):
    """
    Load the configuration file for the specified data type.

    Parameters:
        data_type (str): Type of data to load configuration for.

    Returns:
        dict: Configuration dictionary loaded from the JSON file.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        json.JSONDecodeError: If the configuration file contains invalid JSON.
    """
    base_dir = os.path.dirname(__file__)
    config_path = os.path.join(base_dir, 'config', f'{data_type}.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def create_table_sql(data_type=None):
    """ The function generate create table SQL strings based on SQLite3 by config file.
    :param data_type: Data Type is identifier of data types such as ENTRY, ODDS, RACE and RESULT.
    """
    # Validating Arguments
    if data_type is None:
        raise SystemExit("There is no race_id in HTML")

    # load config file
    keys = [key["col_name"] for key in load_config(data_type)["columns"]]
    types = [tp["var_type"] for tp in load_config(data_type)["columns"]]
    # Create comma separated strings
    cols = [k + ' ' + v for k, v in zip(keys, types)]
    # Add PRIMARY KEY string to first column
    cols[0] = cols[0] + " PRIMARY KEY"
    cols = ", ".join(cols)

    return f"CREATE TABLE IF NOT EXISTS {data_type} ({cols});"

def create_index_sql(data_type=None):
    """ The function generate create index SQL strings based on SQLite3 by config file.
    :param data_type: Data Type is identifier of data types such as ENTRY, ODDS, RACE and RESULT.
    """
    # Validating Arguments
    if data_type == "entry":
        sql = "CREATE INDEX IF NOT EXISTS race_id ON ENTRY (race_id); " \
        "CREATE INDEX IF NOT EXISTS horse_id ON ENTRY (horse_id);"
    elif data_type == "odds":
        sql = ""
    elif data_type == "result":
        sql = "CREATE INDEX IF NOT EXISTS race_id ON RESULT (race_id);" \
        "CREATE INDEX IF NOT EXISTS horse_id ON RESULT (horse_id);"
    elif data_type == "history":
        sql = "CREATE INDEX IF NOT EXISTS race_id ON RESULT (race_id);" \
        "CREATE INDEX IF NOT EXISTS horse_id ON RESULT (horse_id);"
    else:
        raise ValueError(f"Unexpected data type: {data_type}")

    return sql

# Keiba Scraper

[![Test](https://github.com/new-village/keibascraper/actions/workflows/test.yaml/badge.svg?branch=main)](https://github.com/new-village/keibascraper/actions/workflows/unittest.yaml)
[![PyPI](https://badge.fury.io/py/keibascraper.svg)](https://badge.fury.io/py/keibascraper)

**keibascraper** is a Python library designed to parse data from [netkeiba.com](https://www.netkeiba.com/), a prominent Japanese horse racing website. It allows users to programmatically extract detailed information about races, entries, results, odds, and horses. Please note that depending on your usage, this may impose a significant load on netkeiba.com.


## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Dependencies](#dependencies)
- [Usage](#usage)
  - [Loading Entry Data (出走データ)](#loading-entry-data)
  - [Loading Result Data (結果データ)](#loading-result-data)
  - [Loading Odds Data (オッズデータ)](#loading-odds-data)
  - [Loading Horse Data (血統データ/出走履歴データ)](#loading-horse-data)
  - [Bulk Data Loading](#bulk-data-loading)
- [API Reference](#api-reference)
  - [`load` Function](#load-function)
  - [`race_list` Function](#race_list-function)
- [Contributing](#contributing)
- [License](#license)


## Features

- **Flexible Data Loading**: Supports loading of various data types such as race entries, results, odds, and horse information.
- **Configurable Parsing**: Utilizes JSON configuration files to define parsing rules, making it easy to adapt to changes in the source website.
- **Error Handling**: Provides robust error handling to manage network issues and data inconsistencies.
- **Caching**: Implements caching mechanisms to improve performance and reduce redundant network requests.

## Installation

keibascraper is available on PyPI and can be installed using pip:

```bash
$ python -m pip install keibascraper
```

**Supported Python Versions**: keibascraper officially supports Python 3.8 and above.

## Dependencies

- [requests](https://pypi.org/project/requests/): For handling HTTP requests.
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/): For parsing HTML content.
- [jq](https://pypi.org/project/jq/): For parsing JSON content using jq expressions.

## Usage

To use keibascraper, import the library and use the `load` function to fetch and parse data from netkeiba.com. The `load` function requires two parameters: the data type and the entity ID.

### Loading Entry Data (出走データ)

```python
import keibascraper

# Load entry data for a specific race ID
race_id = "202206050811"  # Example race ID
race_info, entry_list = keibascraper.load("entry", race_id)

# Access race information
print(race_info)
# Output: {'race_id': '202206050811', 'race_name': 'Example Race', ...}

# Access entry list
print(entry_list)
# Output: [{'horse_number': 1, 'horse_name': 'Horse A', ...}, {...}, ...]
```

### Loading Result Data (結果データ)

```python
import keibascraper

# Load result data for a specific race ID
race_id = "202206050811"  # Example race ID
race_info, result_list = keibascraper.load("result", race_id)

# Access race information
print(race_info)
# Output: {'race_id': '202206050811', 'race_name': 'Example Race', ...}

# Access result list
print(result_list)
# Output: [{'rank': 1, 'horse_name': 'Horse A', 'rap_time': 120.5, ...}, {...}, ...]
```

### Loading Odds Data (オッズデータ)

```python
import keibascraper

# Load odds data for a specific race ID
race_id = "202206050811"  # Example race ID
odds_data = keibascraper.load("odds", race_id)

# Access odds information
print(odds_data)
# Output: [{'horse_number': 1, 'win': 3.5, 'show_min': 1.2, 'show_max': 1.5, ...}, {...}, ...]
```

### Loading Horse Data (血統データ/出走履歴データ)

```python
import keibascraper

# Load horse data for a specific horse ID
horse_id = "2010101234"  # Example horse ID
horse_info, history_list = keibascraper.load("horse", horse_id)

# Access horse information
print(horse_info)
# Output: {'horse_id': '2010101234', 'horse_name': 'Horse A', 'father_name': 'Sire A', ...}

# Access race history
print(history_list)
# Output: [{'race_date': '2022-06-05', 'race_name': 'Example Race', 'rank': 1, ...}, {...}, ...]
```

### Bulk Data Loading

To load multiple races in bulk, you can use the `race_list` function to retrieve a list of race IDs for a specific year and month.

```python
import keibascraper

# Get list of race IDs for July 2022
race_ids = keibascraper.race_list(2022, 7)

# Loop through race IDs and load entry data
for race_id in race_ids:
    race_info, entry_list = keibascraper.load("entry", race_id)
    # Process the data as needed
```


## API Reference

### `load` Function

```python
keibascraper.load(data_type, entity_id)
```

- **Description**: Loads data from netkeiba.com based on the specified data type and entity ID.
- **Parameters**:
  - `data_type` (str): Type of data to load. Supported types are `'entry'`, `'result'`, `'odds'`, and `'horse'`.
  - `entity_id` (str): Identifier for the data entity (e.g., race ID, horse ID).
- **Returns**:
  - For `'entry'` and `'result'`: Returns a tuple `(race_info, data_list)`.
  - For `'odds'`: Returns a list `odds_data`.
  - For `'horse'`: Returns a tuple `(horse_info, history_list)`.
- **Raises**:
  - `ValueError`: If an unsupported data type is provided.
  - `RuntimeError`: If data loading or parsing fails.

### `race_list` Function

```python
keibascraper.race_list(year, month)
```

- **Description**: Retrieves a list of race IDs for the specified year and month.
- **Parameters**:
  - `year` (int): The target year.
  - `month` (int): The target month.
- **Returns**:
  - A list of race IDs (str).


## Contributing

Contributions are welcome! If you have suggestions or find bugs, please open an issue or submit a pull request on the [GitHub repository](https://github.com/new-village/keibascraper).

When contributing, please follow these guidelines:

- **Coding Standards**: Follow PEP 8 style guidelines.
- **Testing**: Ensure that your code passes existing tests and add new tests for your changes.
- **Documentation**: Update documentation and docstrings as needed.


## License

This project is licensed under the terms of the Apache-2.0 license. See the [LICENSE](https://github.com/new-village/keibascraper/blob/main/LICENSE) file for details.


**Disclaimer**: This library is intended for personal use and educational purposes. Scraping data from websites may violate their terms of service. Please ensure that you comply with netkeiba.com's terms and conditions when using this library.

import os
import pytest
import pandas as pd
from life_expectancy import DATA_DIR, Country
from life_expectancy.cleaning import LifeExpectancyCleaning

@pytest.fixture
def valid_country():
    return Country.DEUTSCHLAND

@pytest.fixture
def valid_cleaning_strategy():
    return "tsv"

@pytest.fixture
def cleaner(valid_country, valid_cleaning_strategy):
    return LifeExpectancyCleaning(valid_country, valid_cleaning_strategy)

# Test to ensure the load, clean, filter, and export process works correctly
def test_load_clean_filter_export_valid(cleaner, valid_country):
    cleaner.load_clean_filter_export()

    # Assert that the cleaned data is exported to a CSV file
    file_path = f'{DATA_DIR}/{valid_country.value.lower()}_life_expectancy.csv'
    assert os.path.exists(file_path)

    # Assert that the exported CSV file contains the cleaned data
    exported_data = pd.read_csv(file_path)
    assert not exported_data.empty

def test_invalid_country_raises_error(valid_cleaning_strategy):
    with pytest.raises(ValueError):
        invalid_country = Country("INVALID_COUNTRY")
        LifeExpectancyCleaning(invalid_country, valid_cleaning_strategy)

def test_invalid_cleaning_strategy_raises_error(valid_country):
    invalid_cleaning_strategy = "invalid_strategy"
    with pytest.raises(ValueError):
        LifeExpectancyCleaning(valid_country, invalid_cleaning_strategy)

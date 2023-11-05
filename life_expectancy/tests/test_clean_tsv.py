import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from life_expectancy import DATA_DIR, TSV_FILE_NAME
from life_expectancy.data_cleaning.clean_tsv import TSVCleaner


def test_instantiation_with_valid_file_name():
    cleaner = TSVCleaner(file_name=TSV_FILE_NAME)
    assert cleaner.file_name == TSV_FILE_NAME

def test_load_raw_data_from_tsv_file():
    cleaner = TSVCleaner(file_name=TSV_FILE_NAME)
    raw_data = cleaner._load_raw_data()
    assert isinstance(raw_data, pd.DataFrame)

def test_melt_table():
    cleaner = TSVCleaner(file_name=TSV_FILE_NAME)
    melted_data = cleaner._melt_table(cleaner.raw_data)
    assert isinstance(melted_data, pd.DataFrame)

def test_tsv_file_does_not_exist():
    with pytest.raises(FileNotFoundError):
        cleaner = TSVCleaner(file_name="nonexistent_file.tsv")
        cleaner._load_raw_data()

def test_tsv_file_is_empty():
    with pytest.raises(pd.errors.EmptyDataError):
        cleaner = TSVCleaner(file_name="empty_file.tsv")
        cleaner._load_raw_data()
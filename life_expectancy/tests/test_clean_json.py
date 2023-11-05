import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from life_expectancy import DATA_DIR, JSON_FILE_NAME
from life_expectancy.data_cleaning.clean_json import JSONCleaner

SAMPLE_JSON_DATA = pd.read_json(f"{DATA_DIR}/{JSON_FILE_NAME}")[100:]

@pytest.fixture
def json_cleaner():
    with patch('pandas.read_json') as mock_read_json:
        mock_read_json.return_value = SAMPLE_JSON_DATA
        cleaner = JSONCleaner(file_name=JSON_FILE_NAME)
        cleaner.raw_data = cleaner._load_raw_data()
        return cleaner

def test_load_raw_data(json_cleaner):
    raw_data = json_cleaner._load_raw_data()
    assert not raw_data.empty
    assert isinstance(raw_data, pd.DataFrame)

def test_unpack_dq_flags(json_cleaner):
    cleand_data = json_cleaner._unpack_dq_flags(json_cleaner.raw_data)
    assert 'flg_ts_break' in cleand_data.columns
    assert 'flg_estimated' in cleand_data.columns
    assert 'flg_provisional' in cleand_data.columns

def test_enforce_dtype(json_cleaner):
    cleand_data = json_cleaner._unpack_dq_flags(json_cleaner.raw_data)
    cleand_data = json_cleaner._enforce_dtype(cleand_data)
    assert cleand_data['unit'].dtype == 'object'
    assert cleand_data['sex'].dtype == 'object'
    assert cleand_data['age'].dtype == 'object'
    assert cleand_data['country'].dtype == 'object'
    assert cleand_data['year'].dtype == 'int64'
    assert cleand_data['life_expectancy'].dtype == 'float64'
    assert cleand_data['flg_ts_break'].dtype == 'bool'
    assert cleand_data['flg_estimated'].dtype == 'bool'
    assert cleand_data['flg_provisional'].dtype == 'bool'

def test_clean(json_cleaner):
    cleand_data = json_cleaner.clean()
    assert not cleand_data.empty
    assert isinstance(cleand_data, pd.DataFrame)
    assert 'flg_ts_break' in cleand_data.columns
    assert 'flg_estimated' in cleand_data.columns
    assert 'flg_provisional' in cleand_data.columns
    assert cleand_data['unit'].dtype == 'object'
    assert cleand_data['sex'].dtype == 'object'
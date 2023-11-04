"""Test the data module."""
from unittest.mock import patch
import pandas as pd
from life_expectancy.data import load_data, save_data_csv

@patch('pandas.read_table')
def test_load_data(mock_read_table):
    """Test the load_data function.

    Args:
        mock_read_table (unittest.mock.MagicMock):
            Mock the pandas.read_table function.
    """
    mock_path = "fake/path"
    mock_read_table.return_value = pd.DataFrame({"column1": [1, 2, 3]})

    data = load_data(mock_path)

    mock_read_table.assert_called_once_with(f'{mock_path}/eu_life_expectancy_raw.tsv')
    assert isinstance(data, pd.DataFrame)

@patch('pandas.DataFrame.to_csv')
def test_save_data_csv(mock_to_csv):
    """Test the save_data_csv function.
    
    Args:
        mock_to_csv (unittest.mock.MagicMock):
            Mock the pandas.DataFrame.to_csv function.
    """
    mock_path = "fake/path"
    mock_data = pd.DataFrame({"column1": [1, 2, 3]})
    mock_region = "Mock Region"

    save_data_csv(mock_path, mock_data, mock_region)

    mock_to_csv.assert_called_once_with(
        f'{mock_path}/{mock_region.lower()}_life_expectancy.csv',
        index=False
    )

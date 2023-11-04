"""Module to clean JSON files"""
import pandas as pd
from life_expectancy.data_cleaning.abstract import AbstractCleaner

class JSONCleaner(AbstractCleaner):
    """Class to clean life_expectancy JSON files
    """
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        super().__init__()

    def clean(self) -> pd.DataFrame:
        """Life expectancy cleaning data process

        Returns:
            pd.DataFrame: Cleaned life expectancy data from JSON file
        """
        cleand_data = self.raw_data.copy()
        cleand_data = self._unpack_dq_flags(cleand_data)
        cleand_data = self._enforce_dtype(cleand_data)

        return cleand_data

    def _load_raw_data(self) -> pd.DataFrame:
        """Load data from JSON file

        Returns:
            pd.DataFrame: life expectancy raw data from JSON file
        """
        return pd.read_json(f"{self.file_dir}/{self.file_name}")

    def _unpack_dq_flags(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """Unpack flag_detail column into seperate bool data quality flags.

        Args:
            cleand_data (pd.DataFrame): Cleaned life expectancy data

        Returns:
            pd.DataFrame: Cleaned data df with data quality flags
        """
        flag_dict = {
            'flg_ts_break': 'break in time series',
            'flg_estimated': 'estimated',
            'flg_provisional': 'provisional'
        }

        for flag in ["flg_ts_break", "flg_estimated", "flg_provisional"]:
            cleand_data[flag] = cleand_data['flag_detail'].str.contains(flag_dict[flag])
            cleand_data[flag].fillna(False, inplace=True)

        return cleand_data.drop(
            columns=["flag", "flag_detail"]
        )
    
    def _enforce_dtype(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """Define the datatype of all cleaned data df columns

        Args:
            cleand_data (pd.DataFrame): Cleaned life expectancy json data

        Returns:
            pd.DataFrame: Cleaned life expectancy data with defined col dtypes
        """
        return cleand_data.astype({
            'unit': 'object',
            'sex': 'object',
            'age': 'object',
            'country': 'object',
            'year': 'int64',
            'life_expectancy': 'float64',
            'flg_ts_break': 'bool',
            'flg_estimated': 'bool',
            'flg_provisional': 'bool'
        })

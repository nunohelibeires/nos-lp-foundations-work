"""Module to clean TSV/CSV files"""
# %%
import os
from pathlib import Path

os.chdir(Path(__file__).parent.parent.parent)
os.getcwd()

# %%
import pandas as pd
from life_expectancy.data_cleaning.abstract import AbstractCleaner

class TSVCleaner(AbstractCleaner):
    """Class to clean life_expectancy TSV/CSV files
    """
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        super().__init__()

    def clean(self) -> pd.DataFrame:
        cleand_data = self.raw_data.copy()
        cleand_data = self._melt_table(cleand_data)
        cleand_data = self._extract_map_dq_flag_detail(cleand_data)
        cleand_data = self._unpack_dq_flags(cleand_data)
        cleand_data = self._clean_year_value_cols(cleand_data)
        cleand_data = self._clean_region_col(cleand_data)
        cleand_data = self._rename_cols(cleand_data)

        return cleand_data

    def _load_raw_data(self) -> pd.DataFrame:
        """Load data from TSV/CSV file

        Returns:
            pd.DataFrame: life expectancy raw data from TSV file
        """
        return pd.read_table(f"{self.file_dir}/{self.file_name}")
    
    def _melt_table(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        # clean column names
        cleand_data[['unit', 'sex', 'age', 'region']] = cleand_data[
            'unit,sex,age,geo\\time'
        ].str.split(',', expand=True)

        cleand_data.drop('unit,sex,age,geo\\time', axis=1, inplace=True)

        # melt table
        return cleand_data.melt(
            id_vars=['unit', 'sex', 'age', 'region'],
            var_name='year', value_name='value'
        )
    
    def _extract_map_dq_flag_detail(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """Extract data quality flag and map to a more descriptive flag.

        Args:
            cleand_data (pd.DataFrame): Cleaned life expectancy data

        Returns:
            pd.DataFrame: Cleaned life expectancy data with data quality
            flag detail column
        """
        cleand_data[['value','flag']] = cleand_data['value'].str.split(' ', expand=True)

        flag_detail_dict = {
            'b': 'break in time series',
            'ep': 'estimated, provisional',
            'p': 'provisional',
            'e': 'estimated',
            'bep': 'break in time series, estimated, provisional'
        }
        cleand_data['flag_detail'] = cleand_data['flag'].map(flag_detail_dict)

        return cleand_data
    
    def _unpack_dq_flags(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """Unpack flag_detail column into seperate bool data quality flags.

        Args:
            cleand_data (pd.DataFrame): Cleaned life expectancy data

        Returns:
            pd.DataFrame: Cleaned data df with data quality flags
        """
        # unpack descriptive flags into boolean data quality flags
        flag_dict = {
            'flg_ts_break': 'break in time series',
            'flg_estimated': 'estimated',
            'flg_provisional': 'provisional'
        }

        for flag in ["flg_ts_break", "flg_estimated", "flg_provisional"]:
            cleand_data[flag] = cleand_data['flag_detail'].str.contains(flag_dict[flag])
            cleand_data[flag].fillna(False, inplace=True)

        return cleand_data.drop(columns=[
            'flag', 'flag_detail'
        ])

    def _clean_year_value_cols(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """Clean the year and value columns, ensure they are of the correct type and
            drop rows with missing values.

        Args:
            cleand_data (pd.DataFrame): Cleaned life expectancy data

        Returns:
            cleand_data (pd.DataFrame): Data with cleaned year and value columns.
        """
        # Ensure year is an integer
        cleand_data['year'] = cleand_data['year'].str.extract(
            r'(\d+)', expand=False
            ).astype(int)

        # Ensure value is a float
        cleand_data['value'] = cleand_data['value'].str.extract(
            r'(\d+.\d+)', expand=False
            ).astype(float)

        # drop rows with missing values
        cleand_data.dropna(inplace=True)

        return cleand_data

    def _clean_region_col(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """
        Clean the region column of the data.

        Args:
            cleand_data: Cleaned life expectancy data

        Returns:
            Cleaned life expectancy data with cleaned region column
        """
        cleand_data['region'] = cleand_data['region'].apply(
            lambda region: region.split('_')[0]
            )

        return cleand_data

    def _rename_cols(self, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """Rename final columns for life expectancy data from TSV file

        Args:
            cleand_data (pd.DataFrame): Cleaned life expectancy data

        Returns:
            pd.DataFrame: Cleaned life expectancy data with renamed cols
        """
        return cleand_data.rename(
            columns={
            'region': 'country',
            'value': 'life_expectancy'
            }
        )

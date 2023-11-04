"""Module to clean TSV/CSV files"""
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
        return cleand_data.rename(
            columns={
            'region': 'country',
            'value': 'life_expectancy'
            }
        )

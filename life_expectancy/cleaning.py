"""Life Expectancy data cleaning pipeline"""

import pandas as pd
from life_expectancy import DATA_DIR, JSON_FILE_NAME, TSV_FILE_NAME, Country
from life_expectancy.data_cleaning.abstract import AbstractCleaner
from life_expectancy.data_cleaning.clean_json import JSONCleaner
from life_expectancy.data_cleaning.clean_tsv import TSVCleaner


class LifeExpectancyCleaning:
    """Class to clean life expectancy data from TSV or JSON files.
    """
    def __init__(
            self,
            country: Country,
            cleaning_strategy: AbstractCleaner
    ) -> None:
        self.country = country
        self.cleaning_strategy = cleaning_strategy
        self._validate_cleaning_strategy()

    def load_clean_filter_export(self) -> None:
        """Main class method that loads, cleans, filters
        and exports life expectancy data"""
        if self.cleaning_strategy == "tsv":
            strategy = TSVCleaner(
                file_name = TSV_FILE_NAME
            )
        elif self.cleaning_strategy == "json":
            strategy = JSONCleaner(
                file_name = JSON_FILE_NAME
            )

        cleand_data = strategy.clean()

        cleand_data = self._filter_country(self.country, cleand_data)

        self._export_cleand_data_to_csv(cleand_data)

    def _export_cleand_data_to_csv(self, cleand_data: pd.DataFrame) -> None:
        """Export data to csv"""
        cleand_data.to_csv(
            f'{DATA_DIR}/{self.country.value.lower()}_life_expectancy.csv',
            index=False
        )

    def _filter_country(self, country: Country, cleand_data: pd.DataFrame) -> pd.DataFrame:
        """Filter data by country enum"""
        if self.country not in Country.actual_countries():
            raise ValueError(
                f"""
                The country '{self.country}' is not supported.
                Please choose from {', '.join(Country.actual_countries())}
                """
            )

        return cleand_data[
            cleand_data['country'] == country.value
        ].reset_index(drop=True)

    def _validate_cleaning_strategy(self) -> None:
        """Validate cleaning strategy string"""
        if self.cleaning_strategy not in ["tsv", "json"]:
            raise ValueError(
                """
                Invalid cleaning strategy.
                Choose from 'json' or 'tsv'.
                """
            )

"""Life Expectancy data cleaning pipeline"""

import pandas as pd
from life_expectancy import DATA_DIR, JSON_FILE_NAME, TSV_FILE_NAME
from life_expectancy.data_cleaning.abstract import AbstractCleaner
from life_expectancy.data_cleaning.clean_json import JSONCleaner
from life_expectancy.data_cleaning.clean_tsv import TSVCleaner


class LifeExpectancyCleaning:
    def __init__(
            self,
            country: str,
            cleaning_strategy: AbstractCleaner
    ) -> None:
        self.country = country
        self.cleaning_strategy = cleaning_strategy

    def load_clean_export(self) -> None:
        if self.cleaning_strategy == "tsv":
            strategy = TSVCleaner(
                file_name = TSV_FILE_NAME
            )
        elif self.cleaning_strategy == "json":
            strategy = JSONCleaner(
                file_name = JSON_FILE_NAME
            )

        cleand_data = strategy.clean()

        self._export_cleand_data_to_csv()

    def _export_cleand_data_to_csv(self, cleand_data: pd.DataFrame) -> None:
        cleand_data.to_csv(
            f'{DATA_DIR}/{self.country.lower()}_life_expectancy.csv',
            index=False
        )

# TODO: parser
# TODO: country ENUM
# TODO: testing
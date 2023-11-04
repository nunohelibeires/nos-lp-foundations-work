"""Module to load and save data."""

import pandas as pd


def load_data(data_path: str) -> pd.DataFrame:
    """Load the data.

    Args:
        data_path: The path to the data.

    Returns:
        The data.
    """
    return pd.read_table(f'{data_path}/eu_life_expectancy_raw.tsv')

def save_data_csv(data_path: str, data: pd.DataFrame, region: str) -> None:
    """Save the data to a csv file.

    Args:
        data (pd.DataFrame): The data.
    """
    data.to_csv(f'{data_path}/{region.lower()}_life_expectancy.csv', index=False)

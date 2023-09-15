"""Module for cleaning life expectancy data."""
import argparse
import pandas as pd

DATA_PATH = 'life_expectancy/data'

def load_data(data_path: str) -> pd.DataFrame:
    """Load the data.

    Args:
        data_path: The path to the data.

    Returns:
        The data.
    """
    return pd.read_table(f'{data_path}/eu_life_expectancy_raw.tsv')

def clean_data(data: pd.DataFrame, region: str) -> None:
    """ Clean the data for a given region.

    Args:
        region: the name of the region to clean
    """
    full_data = (
        data
        .pipe(_melt_table)
        .pipe(_clean_year_value_cols)
        .pipe(_clean_region_col)
    )
    region_data = _select_region(full_data, region)

    return region_data

def save_data_csv(data_path: str, data: pd.DataFrame, region: str) -> None:
    """Save the data to a csv file.

    Args:
        data (pd.DataFrame): The data.
    """
    data.to_csv(f'{data_path}/{region.lower()}_life_expectancy.csv', index=False)

def _melt_table(data: pd.DataFrame) -> pd.DataFrame:
    """Melt the table to long format.
    
    Args:
        data (pd.DataFrame): The data.
        
    Returns:
        data (pd.DataFrame): The data in long format.
    """

    # clean column names
    data[['unit', 'sex', 'age', 'region']] = data['unit,sex,age,geo\\time'].str.split(
        ',', expand=True
    )
    data.drop('unit,sex,age,geo\\time', axis=1, inplace=True)

    # melt table
    return data.melt(
        id_vars=['unit', 'sex', 'age', 'region'],
        var_name='year', value_name='value'
    )

def _clean_year_value_cols(data: pd.DataFrame) -> pd.DataFrame:
    """Clean the year and value columns, ensure they are of the correct type and
        drop rows with missing values.

    Args:
        data (pd.DataFrame): The data.

    Returns:
        data (pd.DataFrame): The data with cleaned year and value columns.
    """
    # Ensure year is an integer
    data['year'] = data['year'].str.extract(
        r'(\d+)', expand=False
        ).astype(int)

    # Ensure value is a float
    data['value'] = data['value'].str.extract(
        r'(\d+.\d+)', expand=False
        ).astype(float)

    # drop rows with missing values
    data.dropna(inplace=True)

    return data

def _clean_region_col(data: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the region column of the data.

    Args:
        data: The data to clean.

    Returns:
        The cleaned data.
    """
    data['region'] = data['region'].apply(
        lambda region: region.split('_')[0]
        )

    return data

def _select_region(data: pd.DataFrame, region: str) -> pd.DataFrame:
    """Select the region.

    Args:
        data (pd.DataFrame): The data.
        region (str): The region to select.

    Returns:
        data (pd.DataFrame): The data with only the specified region.

    Raises:
        ValueError: If the region is not in the data.
    """
    if region not in data['region'].unique():
        raise ValueError(f"""
            The region '{region}' is not found in the data.
            Please choose from {data['region'].unique().tolist()}""")
    return data[data['region'] == region]

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean the data.')
    parser.add_argument(
        '-r',
        '--region',
        type=str,
        default='PT',
        help='The region to select. Defaults to PT.'
    )
    args = parser.parse_args()

    cleaned_data = clean_data(
        data=load_data(DATA_PATH),
        region=args.region
    )

    save_data_csv(DATA_PATH, cleaned_data, args.region)

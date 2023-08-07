import argparse
import pandas as pd

# TODO: cleaning further the region column

def clean_data(region: str) -> None:
    data_path = 'life_expectancy/data'
    df = _load_data(data_path)
    df = _melt_table(df)
    df = _clean_year_value_cols(df)
    df = _select_region(df, region)
    _save_data_csv(data_path, df, region)

def _load_data(data_path: str) -> pd.DataFrame:
    """Load the data from the data folder.

    Returns:
        df (pd.DataFrame): The data.
    """
    df = pd.read_table(f'{data_path}/eu_life_expectancy_raw.tsv')
    return df

def _melt_table(df: pd.DataFrame) -> pd.DataFrame:
    """Melt the table to long format.
    
    Args:
        df (pd.DataFrame): The data.
        
    Returns:
        df (pd.DataFrame): The data in long format.
    """

    # clean column names
    df[['unit', 'sex', 'age', 'region']] = df['unit,sex,age,geo\\time'].str.split(',', expand=True)
    df.drop('unit,sex,age,geo\\time', axis=1, inplace=True)

    # melt table
    df = df.melt(id_vars=['unit', 'sex', 'age', 'region'], var_name='year', value_name='value')

    return df

def _clean_year_value_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the year and value columns, ensure they are of the correct type and
        drop rows with missing values.

    Args:
        df (pd.DataFrame): The data.

    Returns:
        df (pd.DataFrame): The data with cleaned year and value columns.
    """
    # Ensure year is an integer
    df['year'] = df['year'].str.extract(r'(\d+)', expand=False)
    df['year'] = df['year'].astype(int)

    # Ensure value is a float
    df['value'] = df['value'].str.extract(r'(\d+.\d+)', expand=False)
    df['value'] = df['value'].astype(float)

    # drop rows with missing values
    df.dropna(inplace=True)

    return df

def _select_region(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """Select the region.

    Args:
        df (pd.DataFrame): The data.
        region (str): The region to select.

    Returns:
        df (pd.DataFrame): The data with only the specified region.

    Raises:
        ValueError: If the region is not in the data.
    """
    if region not in df['region'].unique():
        raise ValueError(f"The region '{region}' is not found in the data. Please choose from {df['region'].unique().tolist()}")
    
    df = df[df['region'] == region]

    return df

def _save_data_csv(data_path: str, df: pd.DataFrame, region: str) -> None:
    """Save the data to a csv file.

    Args:
        df (pd.DataFrame): The data.
    """
    df.to_csv(f'{data_path}/{region.lower()}_life_expectancy.csv', index=False)

if __name__ == '__main__': # pragma: no cover
    parser = argparse.ArgumentParser(description='Clean the data.')
    parser.add_argument('-r', '--region', type=str, default='PT', help='The region to select. Defaults to PT.')
    args = parser.parse_args()

    clean_data(args.region)
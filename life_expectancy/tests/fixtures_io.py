"""Input/Output operations for fixtures generation."""
# %%
import pandas as pd

from life_expectancy.cleaning import clean_data
from life_expectancy.tests import FIXTURES_DIR, OUTPUT_DIR

def create_raw_sample_data():
    """Create raw sample data."""
    sample_data = pd.read_table(f'{OUTPUT_DIR}/eu_life_expectancy_raw.tsv')[100:]
    sample_data.to_csv(f'{FIXTURES_DIR}/eu_life_expectancy_raw_sample.tsv', sep='\t', index=False)
create_raw_sample_data()

# %%
REGION = 'PT'
def create_expected_clean_data():
    """Create expected clean data."""
    expected_clean_data = clean_data(
        data = pd.read_table(f'{FIXTURES_DIR}/eu_life_expectancy_raw_sample.tsv'),
        region = REGION
    )
    expected_clean_data.to_csv(f'{FIXTURES_DIR}/{REGION.lower()}_life_expectancy_expected.csv', index=False)
create_expected_clean_data()

# %%

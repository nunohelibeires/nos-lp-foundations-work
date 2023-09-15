"""Tests for the cleaning module"""
import pandas as pd

from life_expectancy.cleaning import clean_data
from . import FIXTURES_DIR


def test_clean_data(pt_life_expectancy_expected: pd.DataFrame) -> None:
    """Run the `clean_data` function and compare the output to the expected output"""

    pt_life_expectancy_actual = clean_data(
        data=pd.read_table(f'{FIXTURES_DIR}/eu_life_expectancy_raw_sample.tsv'),
        region='PT'
    )

    pd.testing.assert_frame_equal(
        pt_life_expectancy_actual, pt_life_expectancy_expected
    )

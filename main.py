"""Entrypoint for our Life Expectancy cleaning program"""

import argparse

from life_expectancy import Country
from life_expectancy.cleaning import LifeExpectancyCleaning


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Life expectancy cleaning program"
    )

    parser.add_argument(
        '-c',
        '--country',
        type=Country,
        choices=Country.actual_countries(),
        default='PT',
        help='The region to select. Defaults to PT.'
    )

    parser.add_argument(
        '-s',
        '--strategy',
        type=str,
        choices=["tsv", "json"],
        default='tsv',
        help='Cleaning strategy to select. Defaults to TSV'
    )

    args = parser.parse_args()

    LifeExpectancyCleaning(
        country=args.country,
        cleaning_strategy=args.strategy
    ).load_clean_filter_export()
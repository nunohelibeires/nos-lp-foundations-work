"""Package for life expectancy data."""
from pathlib import Path


DATA_DIR = Path(__file__).parent / "data"
TSV_FILE_NAME = "eu_life_expectancy_raw.tsv"
JSON_FILE_NAME = "eurostat_life_expect.zip"
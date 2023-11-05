import pandas as pd
from life_expectancy import DATA_DIR
from abc import ABC, abstractmethod


class AbstractCleaner(ABC):
    """Abstract class to clean life expectancy files"""

    file_dir: str = DATA_DIR

    def __init__(self) -> None:
        self.raw_data = self._load_raw_data()

    @abstractmethod
    def _load_raw_data(self) -> pd.DataFrame:
        """Abstract method to load data from file"""

    @abstractmethod
    def _unpack_dq_flags(self) -> pd.DataFrame:
        """Unpack flag_detail column into seperate bool data quality flags."""
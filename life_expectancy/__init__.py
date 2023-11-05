"""Package for life expectancy data."""
from enum import Enum
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
TSV_FILE_NAME = "eu_life_expectancy_raw.tsv"
JSON_FILE_NAME = "eurostat_life_expect.zip"

class Country(Enum):
    """Enum class to represent countries"""
    ALBANIA = "AL"
    ARMENIA = "AM"
    AUSTRIA = "AT"
    AZERBAIJAN = "AZ"
    BELARUS = "BY"
    BELGIUM = "BE"
    BULGARIA = "BG"
    CROATIA = "HR"
    CYPRUS = "CY"
    CZECHIA = "CZ"
    DENMARK = "DK"
    DEUTSCHLAND = "DE"
    EAST_WEST_DEUTSCHLAND = "DE_TOT"
    ESTONIA = "EE"
    EUROASIA_18 = "EA18"
    EUROASIA_19 = "EA19"
    EUROPEAN_ECONOMIC_AREA_30 = "EEA30_2007"
    EUROPEAN_ECONOMIC_AREA_31 = "EEA31"
    EUROPEAN_FREE_TRADE_ASSOC = "EFTA"
    EUROPEAN_UNION_27_07 = "EU27_2007"
    EUROPEAN_UNION_27_20 = "EU27_2020"
    EUROPEAN_UNION_28 = "EU28"
    FINLAND = "FI"
    FRANCE = "FR"
    FRANCE_METROPOLITAN = "FX"
    GEORGIA = "GE"
    GREECE = "EL"
    HUNGARY = "HU"
    ICELAND = "IS"
    IRELAND = "IE"
    ITALY = "IT"
    KOSOVO = "XK"
    LATVIA = "LV"
    LIECHTENSTEIN = "LI"
    LITHUANIA = "LT"
    LUXEMBOURG = "LU"
    MALTA = "MT"
    MOLDOVA = "MD"
    MONTENEGRO = "ME"
    NETHERLANDS = "NL"
    NORWAY = "NO"
    POLAND = "PL"
    PORTUGAL = "PT"
    REPUBLIC_OF_NORTH_MACEDONIA = "MK"
    ROMANIA = "RO"
    RUSSIAN_FEDERATION = "RU"
    SAN_MARINO = "SM"
    SERBIA = "RS"
    SLOVAKIA = "SK"
    SLOVENIA = "SI"
    SPAIN = "ES"
    SWEDEN = "SE"
    SWITZERLAND = "CH"
    TURKEY = "TR"
    UKRAINE = "UA"
    UNITED_KINGDOM = "UK"

    @classmethod
    def actual_countries(cls):
        """Return a list of actual country enums, excluding aggregates."""
        aggregates = {"EU27_2020", "DE_TOT", "EA18", "EA19", "EFTA", "EEA30_2007", "EEA31", "EU27_2007", "EU28", "FX"}
        return [country for country in cls if country.name not in aggregates]

"""Chinese astrology calculations for Lunar calendar dates."""

from dataclasses import dataclass

from lunar_python import Lunar


@dataclass
class ChineseAstrology:
    """Chinese astrological information for a Lunar date."""

    is_leap_month: bool
    leap_month_indicator: str
    chinese_year_name: str
    chinese_year_sign: str
    cosmic_element: str
    ming: str
    day_of_week: str


# Mapping of Heavenly Stems (天干) to their associated elements
STEM_TO_ELEMENT = {
    "甲": "Wood",  # Jia
    "乙": "Wood",  # Yi
    "丙": "Fire",  # Bing
    "丁": "Fire",  # Ding
    "戊": "Earth",  # Wu
    "己": "Earth",  # Ji
    "庚": "Metal",  # Geng
    "辛": "Metal",  # Xin
    "壬": "Water",  # Ren
    "癸": "Water",  # Gui
}

# Day of week names (indexed by Solar.getWeek(): 0=Sunday, 1=Monday, ..., 6=Saturday)
WEEKDAY_NAMES = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
]


def get_cosmic_element(heavenly_stem: str) -> str:
    """
    Get the cosmic element from the Heavenly Stem.

    Args:
        heavenly_stem: Chinese character for Heavenly Stem (天干)

    Returns:
        Element name (Wood, Fire, Earth, Metal, Water)
    """
    return STEM_TO_ELEMENT.get(heavenly_stem, "Unknown")


def get_chinese_astrology(lunar: Lunar) -> ChineseAstrology:
    """
    Extract complete Chinese astrological information from a Lunar date.

    Args:
        lunar: Lunar object from lunar_python library

    Returns:
        ChineseAstrology object with all lunar calendar details
    """
    # Get the corresponding Solar date to determine day of week
    solar = lunar.getSolar()
    # Solar.getWeek() returns 0=Sunday, 1=Monday, ..., 6=Saturday
    day_of_week = WEEKDAY_NAMES[solar.getWeek()]

    # Check if this is a leap month
    is_leap = lunar.getMonth() < 0 if hasattr(lunar, "getMonth") else False
    # Alternative check: some versions use different methods
    try:
        month = lunar.getMonth()
        is_leap = month < 0
    except Exception:
        is_leap = False

    leap_indicator = "(Leap Month)" if is_leap else ""

    # Get Chinese year name (e.g., "二〇二四")
    chinese_year_name = lunar.getYearInChinese()

    # Get Chinese zodiac animal (e.g., "龙" Dragon)
    chinese_year_sign = lunar.getYearShengXiao()

    # Get Heavenly Stem and derive cosmic element
    heavenly_stem = lunar.getYearGan()
    cosmic_element = get_cosmic_element(heavenly_stem)

    # Get Ming (命) - the elemental destiny (纳音)
    ming = lunar.getYearNaYin()

    return ChineseAstrology(
        is_leap_month=is_leap,
        leap_month_indicator=leap_indicator,
        chinese_year_name=chinese_year_name,
        chinese_year_sign=chinese_year_sign,
        cosmic_element=cosmic_element,
        ming=ming,
        day_of_week=day_of_week,
    )

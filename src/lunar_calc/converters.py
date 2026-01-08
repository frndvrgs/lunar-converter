"""Calendar conversion orchestration between Gregorian and Chinese Lunar systems."""

from dataclasses import dataclass
from typing import Optional

from lunar_python import Lunar, Solar

from .chinese_astrology import ChineseAstrology, get_chinese_astrology
from .western_astrology import WesternAstrology, get_western_astrology


@dataclass
class GregorianToLunarResult:
    """Result of converting Gregorian to Lunar calendar."""

    # Original Gregorian date
    gregorian_year: int
    gregorian_month: int
    gregorian_day: int
    gregorian_hour: Optional[int]
    gregorian_minute: Optional[int]

    # Converted Lunar date
    lunar_year: int
    lunar_month: int
    lunar_day: int

    # Astrological details
    western: WesternAstrology
    chinese: ChineseAstrology


@dataclass
class LunarToGregorianResult:
    """Result of converting Lunar to Gregorian calendar."""

    # Original Lunar date
    lunar_year: int
    lunar_month: int
    lunar_day: int
    is_leap_month: bool
    lunar_hour: Optional[int]
    lunar_minute: Optional[int]

    # Converted Gregorian date
    gregorian_year: int
    gregorian_month: int
    gregorian_day: int

    # Astrological details
    chinese: ChineseAstrology
    western: WesternAstrology


def gregorian_to_lunar(
    year: int,
    month: int,
    day: int,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
) -> GregorianToLunarResult:
    """
    Convert Gregorian calendar date to Chinese Lunar calendar with astrological details.

    Args:
        year: Gregorian year
        month: Gregorian month (1-12)
        day: Gregorian day (1-31)
        hour: Optional hour (0-23) for more precision
        minute: Optional minute (0-59) for more precision

    Returns:
        GregorianToLunarResult with conversion and astrological data

    Raises:
        ValueError: If date is invalid or out of supported range
    """
    try:
        # Create Solar (Gregorian) date object
        if hour is not None and minute is not None:
            solar = Solar.fromYmdHms(year, month, day, hour, minute, 0)
        else:
            solar = Solar.fromYmd(year, month, day)

        # Convert to Lunar
        lunar = solar.getLunar()

        # Get astrological details
        western = get_western_astrology(year, month, day)
        chinese = get_chinese_astrology(lunar)

        # Extract lunar date components
        lunar_month = lunar.getMonth()
        # Handle leap months (negative values indicate leap)
        is_leap = lunar_month < 0
        lunar_month_abs = abs(lunar_month)

        return GregorianToLunarResult(
            gregorian_year=year,
            gregorian_month=month,
            gregorian_day=day,
            gregorian_hour=hour,
            gregorian_minute=minute,
            lunar_year=lunar.getYear(),
            lunar_month=lunar_month_abs,
            lunar_day=lunar.getDay(),
            western=western,
            chinese=chinese,
        )

    except Exception as e:
        raise ValueError(f"Error converting Gregorian date: {e}") from e


def lunar_to_gregorian(
    year: int,
    month: int,
    day: int,
    is_leap: bool = False,
    hour: Optional[int] = None,
    minute: Optional[int] = None,
) -> LunarToGregorianResult:
    """
    Convert Chinese Lunar calendar date to Gregorian calendar with astrological details.

    Args:
        year: Lunar year
        month: Lunar month (1-12)
        day: Lunar day (1-30)
        is_leap: Whether this is a leap month
        hour: Optional hour (0-23) for more precision
        minute: Optional minute (0-59) for more precision

    Returns:
        LunarToGregorianResult with conversion and astrological data

    Raises:
        ValueError: If date is invalid or out of supported range
    """
    try:
        # Create Lunar date object
        if hour is not None and minute is not None:
            lunar = Lunar.fromYmdHms(year, month, day, hour, minute, 0, is_leap)
        else:
            lunar = Lunar.fromYmd(year, month, day, is_leap)

        # Convert to Solar (Gregorian)
        solar = lunar.getSolar()

        # Get astrological details
        chinese = get_chinese_astrology(lunar)
        western = get_western_astrology(solar.getYear(), solar.getMonth(), solar.getDay())

        return LunarToGregorianResult(
            lunar_year=year,
            lunar_month=month,
            lunar_day=day,
            is_leap_month=is_leap,
            lunar_hour=hour,
            lunar_minute=minute,
            gregorian_year=solar.getYear(),
            gregorian_month=solar.getMonth(),
            gregorian_day=solar.getDay(),
            chinese=chinese,
            western=western,
        )

    except Exception as e:
        raise ValueError(f"Error converting Lunar date: {e}") from e

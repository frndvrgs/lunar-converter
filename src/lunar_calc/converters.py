"""Calendar conversion orchestration between Gregorian and Chinese Lunar systems."""

from dataclasses import dataclass

from lunar_python import Lunar, Solar

from .chinese_astrology import ChineseAstrology, get_chinese_astrology
from .western_astrology import WesternAstrology, get_western_astrology


def is_early_zi_hour(hour: int | None, minute: int | None = None) -> bool:
    """
    Check if the given time falls within the early Zi hour (早子时/夜子时).

    In traditional Chinese time-keeping, the Zi hour (子时) spans from 11 PM to 1 AM.
    The period from 23:00 to 23:59 is called "early Zi hour" (早子时) or "night Zi hour" (夜子时).

    According to traditional Chinese astrology/calendar systems, this early Zi hour
    is considered the START of the next day, not the end of the current day.

    Args:
        hour: Hour in 24-hour format (0-23)
        minute: Minute (0-59), optional

    Returns:
        True if the time is in early Zi hour (23:00-23:59), False otherwise
    """
    if hour is None:
        return False
    return hour == 23


@dataclass
class GregorianToLunarResult:
    """Result of converting Gregorian to Lunar calendar."""

    # Original Gregorian date
    gregorian_year: int
    gregorian_month: int
    gregorian_day: int
    gregorian_hour: int | None
    gregorian_minute: int | None

    # Converted Lunar date
    lunar_year: int
    lunar_month: int
    lunar_day: int

    # Astrological details
    western: WesternAstrology
    chinese: ChineseAstrology

    # Early Zi hour adjustment indicator
    early_zi_hour_adjusted: bool = False


@dataclass
class LunarToGregorianResult:
    """Result of converting Lunar to Gregorian calendar."""

    # Original Lunar date
    lunar_year: int
    lunar_month: int
    lunar_day: int
    is_leap_month: bool
    lunar_hour: int | None
    lunar_minute: int | None

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
    hour: int | None = None,
    minute: int | None = None,
    use_traditional_zi_hour: bool = True,
) -> GregorianToLunarResult:
    """
    Convert Gregorian calendar date to Chinese Lunar calendar with astrological details.

    Args:
        year: Gregorian year
        month: Gregorian month (1-12)
        day: Gregorian day (1-31)
        hour: Optional hour (0-23) for more precision
        minute: Optional minute (0-59) for more precision
        use_traditional_zi_hour: If True (default), times between 23:00-23:59
            will be treated as the next day according to traditional Chinese
            calendar rules where the Zi hour (子时, 11PM-1AM) marks the start
            of a new day. This affects the lunar date calculation for births
            occurring during the "early Zi hour" (早子时).

    Returns:
        GregorianToLunarResult with conversion and astrological data

    Raises:
        ValueError: If date is invalid or out of supported range
    """
    try:
        # Check if we need to apply the traditional Zi hour adjustment
        # In traditional Chinese time-keeping, 23:00-23:59 is considered
        # the early part of Zi hour (早子时) and belongs to the NEXT day
        early_zi_adjusted = False
        adjusted_year, adjusted_month, adjusted_day = year, month, day

        if use_traditional_zi_hour and is_early_zi_hour(hour, minute):
            # Advance to the next day for lunar date calculation
            # We use the library's built-in day advancement to handle month/year rollovers
            temp_solar = Solar.fromYmd(year, month, day)
            next_day_solar = temp_solar.next(1)
            adjusted_year = next_day_solar.getYear()
            adjusted_month = next_day_solar.getMonth()
            adjusted_day = next_day_solar.getDay()
            early_zi_adjusted = True

        # Create Solar (Gregorian) date object for lunar conversion
        # Use the adjusted date if early Zi hour adjustment was applied
        if hour is not None and minute is not None:
            solar = Solar.fromYmdHms(adjusted_year, adjusted_month, adjusted_day, hour, minute, 0)
        else:
            solar = Solar.fromYmd(adjusted_year, adjusted_month, adjusted_day)

        # Convert to Lunar
        lunar = solar.getLunar()

        # Get astrological details (use original date for western astrology)
        western = get_western_astrology(year, month, day)
        chinese = get_chinese_astrology(lunar)

        # Extract lunar date components
        lunar_month = lunar.getMonth()
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
            early_zi_hour_adjusted=early_zi_adjusted,
        )

    except Exception as e:
        raise ValueError(f"Error converting Gregorian date: {e}") from e


def lunar_to_gregorian(
    year: int,
    month: int,
    day: int,
    is_leap: bool = False,
    hour: int | None = None,
    minute: int | None = None,
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
        # lunar-python uses negative month values to represent leap months
        # e.g., leap month 4 is represented as -4
        lunar_month = -month if is_leap else month

        if hour is not None and minute is not None:
            lunar = Lunar.fromYmdHms(year, lunar_month, day, hour, minute, 0)
        else:
            lunar = Lunar.fromYmd(year, lunar_month, day)

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

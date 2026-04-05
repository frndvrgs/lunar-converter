from dataclasses import dataclass

from lunar_python import Lunar, Solar

from .chinese_astrology import ChineseAstrology, get_chinese_astrology
from .western_astrology import WesternAstrology, get_western_astrology


def is_early_zi_hour(hour: int | None, minute: int | None = None) -> bool:
    """Check if the time falls within the early Zi hour (早子时, 23:00-23:59).

    In traditional Chinese time-keeping, 23:00-23:59 is the start of the next day.
    """
    if hour is None:
        return False
    return hour == 23


@dataclass
class GregorianToLunarResult:
    gregorian_year: int
    gregorian_month: int
    gregorian_day: int
    gregorian_hour: int | None
    gregorian_minute: int | None
    lunar_year: int
    lunar_month: int
    lunar_day: int
    western: WesternAstrology
    chinese: ChineseAstrology
    early_zi_hour_adjusted: bool = False


@dataclass
class LunarToGregorianResult:
    lunar_year: int
    lunar_month: int
    lunar_day: int
    is_leap_month: bool
    lunar_hour: int | None
    lunar_minute: int | None
    gregorian_year: int
    gregorian_month: int
    gregorian_day: int
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
    try:
        early_zi_adjusted = False
        adjusted_year, adjusted_month, adjusted_day = year, month, day

        if use_traditional_zi_hour and is_early_zi_hour(hour, minute):
            temp_solar = Solar.fromYmd(year, month, day)
            next_day_solar = temp_solar.next(1)
            adjusted_year = next_day_solar.getYear()
            adjusted_month = next_day_solar.getMonth()
            adjusted_day = next_day_solar.getDay()
            early_zi_adjusted = True

        if hour is not None and minute is not None:
            solar = Solar.fromYmdHms(adjusted_year, adjusted_month, adjusted_day, hour, minute, 0)
        else:
            solar = Solar.fromYmd(adjusted_year, adjusted_month, adjusted_day)

        lunar = solar.getLunar()

        western = get_western_astrology(year, month, day)
        chinese = get_chinese_astrology(lunar)

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
    try:
        # lunar-python uses negative month values for leap months (e.g., leap month 4 = -4)
        lunar_month = -month if is_leap else month

        if hour is not None and minute is not None:
            lunar = Lunar.fromYmdHms(year, lunar_month, day, hour, minute, 0)
        else:
            lunar = Lunar.fromYmd(year, lunar_month, day)

        solar = lunar.getSolar()

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

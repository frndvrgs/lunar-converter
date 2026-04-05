from dataclasses import dataclass
from datetime import date


@dataclass
class WesternAstrology:
    sun_sign: str
    sun_sign_element: str
    day_of_week: str


# Tropical zodiac date ranges
ZODIAC_SIGNS = [
    ("Capricorn", (12, 22), (1, 19)),
    ("Aquarius", (1, 20), (2, 18)),
    ("Pisces", (2, 19), (3, 20)),
    ("Aries", (3, 21), (4, 19)),
    ("Taurus", (4, 20), (5, 20)),
    ("Gemini", (5, 21), (6, 20)),
    ("Cancer", (6, 21), (7, 22)),
    ("Leo", (7, 23), (8, 22)),
    ("Virgo", (8, 23), (9, 22)),
    ("Libra", (9, 23), (10, 22)),
    ("Scorpio", (10, 23), (11, 21)),
    ("Sagittarius", (11, 22), (12, 21)),
]

SIGN_ELEMENTS = {
    "Aries": "Fire",
    "Leo": "Fire",
    "Sagittarius": "Fire",
    "Taurus": "Earth",
    "Virgo": "Earth",
    "Capricorn": "Earth",
    "Gemini": "Air",
    "Libra": "Air",
    "Aquarius": "Air",
    "Cancer": "Water",
    "Scorpio": "Water",
    "Pisces": "Water",
}

WEEKDAY_NAMES = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def calculate_sun_sign(month: int, day: int) -> str:
    for sign, (start_month, start_day), (end_month, end_day) in ZODIAC_SIGNS:
        if start_month > end_month:
            if month == start_month and day >= start_day:
                return sign
            if month == end_month and day <= end_day:
                return sign
        else:
            if month == start_month and day >= start_day:
                return sign
            if month == end_month and day <= end_day:
                return sign
            if start_month < month < end_month:
                return sign

    return "Unknown"


def get_western_astrology(year: int, month: int, day: int) -> WesternAstrology:
    gregorian_date = date(year, month, day)

    sun_sign = calculate_sun_sign(month, day)
    sun_sign_element = SIGN_ELEMENTS.get(sun_sign, "Unknown")
    day_of_week = WEEKDAY_NAMES[gregorian_date.weekday()]

    return WesternAstrology(
        sun_sign=sun_sign,
        sun_sign_element=sun_sign_element,
        day_of_week=day_of_week,
    )

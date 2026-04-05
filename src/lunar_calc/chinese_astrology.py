from dataclasses import dataclass

from lunar_python import Lunar


@dataclass
class ChineseAstrology:
    is_leap_month: bool
    leap_month_indicator: str
    chinese_year_name: str
    chinese_year_sign: str
    cosmic_element: str
    ming: str
    day_of_week: str


# Heavenly Stems (天干) to element mapping
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

# Chinese Zodiac animals with Pinyin
ZODIAC_TO_ENGLISH = {
    "鼠": "Rat (Shǔ)",
    "牛": "Ox (Niú)",
    "虎": "Tiger (Hǔ)",
    "兔": "Rabbit (Tù)",
    "龙": "Dragon (Lóng)",
    "蛇": "Snake (Shé)",
    "马": "Horse (Mǎ)",
    "羊": "Goat (Yáng)",
    "猴": "Monkey (Hóu)",
    "鸡": "Rooster (Jī)",
    "狗": "Dog (Gǒu)",
    "猪": "Pig (Zhū)",
}

# Solar.getWeek(): 0=Sunday, 1=Monday, ..., 6=Saturday
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
    return STEM_TO_ELEMENT.get(heavenly_stem, "Unknown")


def translate_zodiac_sign(chinese_sign: str) -> str:
    return ZODIAC_TO_ENGLISH.get(chinese_sign, chinese_sign)


def get_chinese_astrology(lunar: Lunar) -> ChineseAstrology:
    solar = lunar.getSolar()
    day_of_week = WEEKDAY_NAMES[solar.getWeek()]

    try:
        month = lunar.getMonth()
        is_leap = month < 0
    except Exception:
        is_leap = False

    leap_indicator = "(Leap Month)" if is_leap else ""

    chinese_year_name = lunar.getYearInChinese()
    chinese_year_sign = translate_zodiac_sign(lunar.getYearShengXiao())
    cosmic_element = get_cosmic_element(lunar.getYearGan())
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

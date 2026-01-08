"""Display formatting for calendar conversion results."""

from .converters import GregorianToLunarResult, LunarToGregorianResult


# ANSI color codes for enhanced terminal output
class Colors:
    """ANSI color codes for terminal output."""

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def format_time(hour: int | None, minute: int | None) -> str:
    """Format time components into HH:MM string."""
    if hour is not None and minute is not None:
        return f"{hour:02d}:{minute:02d}"
    return "Not specified"


def display_gregorian_to_lunar(result: GregorianToLunarResult) -> None:
    """
    Display the result of Gregorian to Lunar conversion with formatting.

    Args:
        result: GregorianToLunarResult object
    """
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

    # Original Western Date Section
    print(f"{Colors.BOLD}{Colors.OKBLUE}WESTERN CALENDAR (Solar){Colors.ENDC}")
    print(
        f"{Colors.OKCYAN}Date:{Colors.ENDC} {result.gregorian_year}-{result.gregorian_month:02d}-{result.gregorian_day:02d}"
    )
    print(
        f"{Colors.OKCYAN}Time:{Colors.ENDC} {format_time(result.gregorian_hour, result.gregorian_minute)}"
    )
    print(f"{Colors.OKCYAN}Day of Week:{Colors.ENDC} {result.western.day_of_week}")
    print(
        f"{Colors.OKCYAN}Sun Sign:{Colors.ENDC} {result.western.sun_sign} ({result.western.sun_sign_element})"
    )
    print()

    # Converted Lunar Date Section
    print(f"{Colors.BOLD}{Colors.OKGREEN}CHINESE CALENDAR (Lunar){Colors.ENDC}")
    leap_indicator = (
        f" {Colors.WARNING}{result.chinese.leap_month_indicator}{Colors.ENDC}"
        if result.chinese.is_leap_month
        else ""
    )
    print(
        f"{Colors.OKCYAN}Date:{Colors.ENDC} {result.lunar_year}-{result.lunar_month:02d}-{result.lunar_day:02d}{leap_indicator}"
    )
    # Show early Zi hour adjustment note if applicable
    if result.early_zi_hour_adjusted:
        print(f"{Colors.WARNING}Note:{Colors.ENDC} Birth time is in early Zi hour (23:00-23:59).")
        print("      Traditional Chinese calendar counts this as the next day.")
    print(f"{Colors.OKCYAN}Chinese Year:{Colors.ENDC} {result.chinese.chinese_year_name}")
    print(f"{Colors.OKCYAN}Zodiac Sign:{Colors.ENDC} {result.chinese.chinese_year_sign}")
    print(f"{Colors.OKCYAN}Cosmic Element:{Colors.ENDC} {result.chinese.cosmic_element}")
    print(f"{Colors.OKCYAN}Ming (命):{Colors.ENDC} {result.chinese.ming}")
    print(f"{Colors.OKCYAN}Day of Week:{Colors.ENDC} {result.chinese.day_of_week}")
    print()
    print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def display_lunar_to_gregorian(result: LunarToGregorianResult) -> None:
    """
    Display the result of Lunar to Gregorian conversion with formatting.

    Args:
        result: LunarToGregorianResult object
    """
    print(f"\n{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")

    # Original Lunar Date Section
    print(f"{Colors.BOLD}{Colors.OKGREEN}CHINESE CALENDAR (Lunar){Colors.ENDC}")
    leap_indicator = (
        f" {Colors.WARNING}{result.chinese.leap_month_indicator}{Colors.ENDC}"
        if result.is_leap_month
        else ""
    )
    print(
        f"{Colors.OKCYAN}Date:{Colors.ENDC} {result.lunar_year}-{result.lunar_month:02d}-{result.lunar_day:02d}{leap_indicator}"
    )
    print(
        f"{Colors.OKCYAN}Time:{Colors.ENDC} {format_time(result.lunar_hour, result.lunar_minute)}"
    )
    print(f"{Colors.OKCYAN}Chinese Year:{Colors.ENDC} {result.chinese.chinese_year_name}")
    print(f"{Colors.OKCYAN}Zodiac Sign:{Colors.ENDC} {result.chinese.chinese_year_sign}")
    print(f"{Colors.OKCYAN}Cosmic Element:{Colors.ENDC} {result.chinese.cosmic_element}")
    print(f"{Colors.OKCYAN}Ming (命):{Colors.ENDC} {result.chinese.ming}")
    print(f"{Colors.OKCYAN}Day of Week:{Colors.ENDC} {result.chinese.day_of_week}")
    print()

    # Converted Western Date Section
    print(f"{Colors.BOLD}{Colors.OKBLUE}WESTERN CALENDAR (Solar){Colors.ENDC}")
    print(
        f"{Colors.OKCYAN}Date:{Colors.ENDC} {result.gregorian_year}-{result.gregorian_month:02d}-{result.gregorian_day:02d}"
    )
    print(f"{Colors.OKCYAN}Day of Week:{Colors.ENDC} {result.western.day_of_week}")
    print(
        f"{Colors.OKCYAN}Sun Sign:{Colors.ENDC} {result.western.sun_sign} ({result.western.sun_sign_element})"
    )
    print()
    print(f"{Colors.BOLD}{'=' * 70}{Colors.ENDC}\n")


def display_error(message: str) -> None:
    """
    Display an error message with formatting.

    Args:
        message: Error message to display
    """
    print(f"\n{Colors.FAIL}{Colors.BOLD}ERROR:{Colors.ENDC} {message}\n")

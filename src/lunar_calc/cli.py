import questionary

from .converters import gregorian_to_lunar, lunar_to_gregorian
from .display import display_error, display_gregorian_to_lunar, display_lunar_to_gregorian


def get_integer_input(prompt: str, min_val: int, max_val: int) -> int | None:
    while True:
        response = questionary.text(prompt).ask()

        if response is None:
            return None

        if response.strip() == "":
            return None

        try:
            value = int(response)
            if min_val <= value <= max_val:
                return value
            print(f"Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print("Please enter a valid number.")


def gregorian_to_lunar_flow() -> None:
    print("\n--- Western to Chinese Lunar Calendar ---")

    year = get_integer_input("Enter Western year (e.g., 1990): ", 1900, 2100)
    if year is None:
        return

    month = get_integer_input("Enter month (1-12): ", 1, 12)
    if month is None:
        return

    day = get_integer_input("Enter day (1-31): ", 1, 31)
    if day is None:
        return

    include_time = questionary.confirm(
        "Do you want to include time for more precision?", default=False
    ).ask()

    hour = None
    minute = None

    if include_time:
        hour = get_integer_input("Enter hour (0-23): ", 0, 23)
        if hour is None:
            return

        minute = get_integer_input("Enter minute (0-59): ", 0, 59)
        if minute is None:
            return

    try:
        result = gregorian_to_lunar(year, month, day, hour, minute)
        display_gregorian_to_lunar(result)
    except ValueError as e:
        display_error(str(e))


def lunar_to_gregorian_flow() -> None:
    print("\n--- Chinese Lunar to Western Calendar ---")

    year = get_integer_input("Enter Lunar year (e.g., 1990): ", 1900, 2100)
    if year is None:
        return

    month = get_integer_input("Enter lunar month (1-12): ", 1, 12)
    if month is None:
        return

    day = get_integer_input("Enter lunar day (1-30): ", 1, 30)
    if day is None:
        return

    is_leap = questionary.confirm("Is this a leap month (闰月)?", default=False).ask()

    include_time = questionary.confirm(
        "Do you want to include time for more precision?", default=False
    ).ask()

    hour = None
    minute = None

    if include_time:
        hour = get_integer_input("Enter hour (0-23): ", 0, 23)
        if hour is None:
            return

        minute = get_integer_input("Enter minute (0-59): ", 0, 59)
        if minute is None:
            return

    try:
        result = lunar_to_gregorian(year, month, day, is_leap, hour, minute)
        display_lunar_to_gregorian(result)
    except ValueError as e:
        display_error(str(e))


def run_cli() -> None:
    print("\n🌙 Lunar Calendar Birthday Converter 🌙")
    print("Convert between Western and Chinese Lunar calendars\n")

    while True:
        choice = questionary.select(
            "Select conversion type:",
            choices=[
                "Western to Chinese Lunar",
                "Chinese Lunar to Western",
                "Exit",
            ],
            use_arrow_keys=True,
        ).ask()

        if choice is None or choice == "Exit":
            print("\nGoodbye! 再见!\n")
            break

        if choice == "Western to Chinese Lunar":
            gregorian_to_lunar_flow()
        elif choice == "Chinese Lunar to Western":
            lunar_to_gregorian_flow()

        input("\nPress Enter to continue...")

# 🌙 Lunar Calendar Birthday Converter

A Python CLI tool for converting between Gregorian and Chinese Lunar calendar birthdays with comprehensive astrological details.

## Features

- **Bidirectional Conversion**: Convert dates between Gregorian and Chinese Lunar calendars
- **Precise Calculations**: Uses the `lunar-python` library for mathematically accurate conversions
- **Optional Time Precision**: Include hour and minute for more accurate calculations
- **Western Astrology**: Sun sign, element, and day of week for Gregorian dates
- **Chinese Astrology**: Zodiac animal, cosmic element, Ming (命), and year names for Lunar dates
- **Interactive CLI**: Arrow-key navigation with `questionary`
- **Leap Month Support**: Properly handles Chinese calendar leap months (闰月)

## Installation

This project uses `uv` for Python package management. Install dependencies with:

```bash
uv sync
```

Alternatively, using pip:

```bash
pip install -e .
```

## Usage

### Run the CLI

```bash
uv run python -m lunar_calc
```

Or if installed as a script:

```bash
lunar-calc
```

### Main Menu

The CLI presents an interactive menu with arrow-key navigation:

1. **Gregorian to Chinese Lunar** - Convert a Gregorian date to Lunar calendar
2. **Chinese Lunar to Gregorian** - Convert a Lunar date to Gregorian calendar
3. **Exit** - Quit the application

### Input Options

For each conversion, you'll be prompted for:

- **Year, Month, Day** (required)
- **Hour and Minute** (optional) - For more precise calculations
- **Leap Month Status** (Lunar to Gregorian only) - Whether the month is a leap month

## Output Details

### Gregorian Date Information

- **Date**: YYYY-MM-DD format
- **Time**: HH:MM (if provided)
- **Day of Week**: Full weekday name
- **Sun Sign**: Astrological zodiac sign based on tropical zodiac
- **Sun Sign Element**: Fire, Earth, Air, or Water

### Chinese Lunar Date Information

- **Date**: YYYY-MM-DD format with leap month indicator (闰月)
- **Chinese Year Name**: Year in Chinese characters (e.g., 二〇二四)
- **Zodiac Sign**: Chinese zodiac animal (e.g., 龙 Dragon)
- **Cosmic Element**: Element derived from Heavenly Stem (Wood, Fire, Earth, Metal, Water)
- **Ming (命)**: Elemental destiny (纳音 Nayin)
- **Day of Week**: Full weekday name

## How It Works

### Calendar Systems

**Gregorian Calendar**: The standard international solar calendar with 12 months of fixed lengths.

**Chinese Lunar Calendar**: A lunisolar calendar based on moon phases, with years of 12 or 13 months (leap years). Months are 29 or 30 days long, and leap months (闰月) are added approximately every 3 years to align with the solar year.

### Astrological Calculations

**Western Astrology**: Sun signs are calculated using tropical zodiac date ranges (e.g., Aries: March 21 - April 19).

**Chinese Astrology**: 
- **Zodiac Animal** (生肖): Based on the Chinese year (12-year cycle)
- **Heavenly Stems** (天干): 10-year cycle determining cosmic elements
- **Earthly Branches** (地支): 12-year cycle associated with zodiac animals
- **Nayin** (纳音): 60-year cycle determining Ming (elemental destiny)

### Timezone Handling

The tool uses your system's local timezone for date calculations. No explicit timezone conversion is performed, ensuring dates are interpreted in your local context.

## Supported Date Range

The underlying `lunar-python` library supports dates from **1900 to 2100**.

## Development

### Project Structure

```
lunar-calc/
├── pyproject.toml          # Project configuration and dependencies
├── README.md               # This file
└── src/
    └── lunar_calc/
        ├── __init__.py           # Package initialization
        ├── __main__.py           # CLI entry point
        ├── cli.py                # Interactive menu and input handling
        ├── converters.py         # Conversion orchestration
        ├── chinese_astrology.py  # Lunar calendar details extraction
        ├── western_astrology.py  # Gregorian calendar astrology
        └── display.py            # Output formatting
```

### Code Quality

The project uses `ruff` for linting and formatting:

```bash
# Format code
uv run ruff format .

# Lint code
uv run ruff check .
```

## Dependencies

- **lunar-python** (>=1.6.0): Comprehensive Chinese calendar library
- **questionary** (>=2.0.0): Interactive CLI prompts with arrow-key navigation

## License

This project is provided as-is for calendar conversion and educational purposes.

## Credits

- **lunar-python** by 6tail - Provides the core calendar conversion algorithms
- **questionary** - Powers the interactive CLI experience

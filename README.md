# lunar-calc

Gregorian and Chinese Lunar calendar converter with astrological details.

## Install

```bash
pip install lunar-calc
```

## Usage

```bash
lunar-calc
```

Interactive CLI with arrow-key navigation:
- Gregorian → Chinese Lunar
- Chinese Lunar → Gregorian

## Output

For each conversion:
- Gregorian: date, day of week, sun sign, element
- Lunar: date, Chinese year name, zodiac animal, cosmic element, Ming (命)

## API

```python
from lunar_calc import gregorian_to_lunar, lunar_to_gregorian

result = gregorian_to_lunar(1990, 6, 15)
result = lunar_to_gregorian(1990, 5, 23)
```

## License

MIT

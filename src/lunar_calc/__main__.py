"""Entry point for the lunar-calc CLI application."""

import sys

from .cli import run_cli


def main() -> None:
    """Main entry point for the application."""
    try:
        run_cli()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Goodbye! 再见!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

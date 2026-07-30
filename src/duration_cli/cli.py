"""Command-line entry point for duration-cli."""
from __future__ import annotations

import argparse
import sys

from .core import format_duration, parse_duration


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="duration-cli",
        description="Convert between human-readable durations and total seconds, "
        "auto-detecting direction from the input.",
    )
    parser.add_argument(
        "value",
        help="A bare number of seconds (e.g. 90) or a human duration (e.g. 2h30m, "
        "'1d 4h', 90s)",
    )
    return parser


def _is_bare_number(text: str) -> bool:
    try:
        float(text.strip())
        return True
    except ValueError:
        return False


def main(argv: "list[str] | None" = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    value = args.value

    if _is_bare_number(value):
        seconds = float(value)
        if seconds < 0:
            print("duration-cli: error: seconds must be non-negative", file=sys.stderr)
            return 2
        print(format_duration(seconds))
        return 0

    try:
        seconds = parse_duration(value)
    except ValueError as exc:
        print(f"duration-cli: error: {exc}", file=sys.stderr)
        return 2

    print(seconds)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Core parsing and formatting logic for duration-cli."""
from __future__ import annotations

import re

UNIT_SECONDS: dict[str, int] = {
    "s": 1,
    "m": 60,
    "h": 3600,
    "d": 86400,
    "w": 604800,
}

_TOKEN_RE = re.compile(r"(\d+(?:\.\d+)?)([smhdw])")
_VALID_RE = re.compile(r"(?:\d+(?:\.\d+)?[smhdw])+")


def parse_duration(text: str) -> int:
    """Parse a human-readable duration ("2h30m", "1d 4h", "90s") into total seconds.

    Units may be separated by whitespace or written back-to-back. Supported
    units are s(econds), m(inutes), h(ours), d(ays), and w(eeks). Raises
    ValueError if the string isn't a valid duration.
    """
    if text is None:
        raise ValueError("duration string must not be None")
    compact = re.sub(r"\s+", "", text.strip()).lower()
    if not compact or not _VALID_RE.fullmatch(compact):
        raise ValueError(f"not a valid duration string: {text!r}")

    total = 0.0
    for amount, unit in _TOKEN_RE.findall(compact):
        total += float(amount) * UNIT_SECONDS[unit]
    return int(round(total))


def format_duration(seconds: float) -> str:
    """Format a number of seconds as a compact human-readable duration.

    E.g. 9000 -> "2h30m", 90 -> "1m30s", 0 -> "0s". Negative values are
    formatted with a leading "-".
    """
    total = int(round(seconds))
    negative = total < 0
    remaining = abs(total)

    parts: list[str] = []
    for unit in ("w", "d", "h", "m", "s"):
        unit_seconds = UNIT_SECONDS[unit]
        value, remaining = divmod(remaining, unit_seconds)
        if value:
            parts.append(f"{value}{unit}")

    result = "".join(parts) if parts else "0s"
    return f"-{result}" if negative else result

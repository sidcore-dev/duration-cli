import unittest

from duration_cli.core import format_duration, parse_duration


class TestParseDuration(unittest.TestCase):
    def test_single_unit(self) -> None:
        self.assertEqual(parse_duration("90s"), 90)

    def test_compact_multiple_units(self) -> None:
        self.assertEqual(parse_duration("2h30m"), 9000)

    def test_spaced_multiple_units(self) -> None:
        self.assertEqual(parse_duration("1d 4h"), 86400 + 4 * 3600)

    def test_week_unit(self) -> None:
        self.assertEqual(parse_duration("2w"), 2 * 604800)

    def test_uppercase_units(self) -> None:
        self.assertEqual(parse_duration("2H30M"), 9000)

    def test_decimal_amount(self) -> None:
        self.assertEqual(parse_duration("1.5h"), 5400)

    def test_invalid_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_duration("not a duration")

    def test_empty_string_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_duration("")

    def test_unknown_unit_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_duration("5x")


class TestFormatDuration(unittest.TestCase):
    def test_zero(self) -> None:
        self.assertEqual(format_duration(0), "0s")

    def test_seconds_only(self) -> None:
        self.assertEqual(format_duration(45), "45s")

    def test_minutes_and_seconds(self) -> None:
        self.assertEqual(format_duration(90), "1m30s")

    def test_hours_and_minutes(self) -> None:
        self.assertEqual(format_duration(9000), "2h30m")

    def test_days_and_hours(self) -> None:
        self.assertEqual(format_duration(86400 + 4 * 3600), "1d4h")

    def test_weeks(self) -> None:
        self.assertEqual(format_duration(2 * 604800), "2w")

    def test_negative_value(self) -> None:
        self.assertEqual(format_duration(-90), "-1m30s")

    def test_roundtrip(self) -> None:
        seconds = 93784  # 1d 2h 3m 4s
        formatted = format_duration(seconds)
        self.assertEqual(parse_duration(formatted), seconds)


if __name__ == "__main__":
    unittest.main()

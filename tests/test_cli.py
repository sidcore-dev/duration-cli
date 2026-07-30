import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from duration_cli.cli import main


class TestCli(unittest.TestCase):
    def test_bare_number_converts_to_human(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["9000"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "2h30m")

    def test_human_string_converts_to_seconds(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["2h30m"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "9000")

    def test_spaced_human_string(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["1d 4h"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), str(86400 + 4 * 3600))

    def test_bare_seconds_string(self) -> None:
        out = io.StringIO()
        with redirect_stdout(out):
            code = main(["90s"])
        self.assertEqual(code, 0)
        self.assertEqual(out.getvalue().strip(), "90")

    def test_negative_bare_number_errors(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["-5"])
        self.assertEqual(code, 2)
        self.assertIn("non-negative", err.getvalue())

    def test_invalid_input_errors(self) -> None:
        err = io.StringIO()
        with redirect_stderr(err):
            code = main(["banana"])
        self.assertEqual(code, 2)
        self.assertIn("not a valid duration", err.getvalue())


if __name__ == "__main__":
    unittest.main()

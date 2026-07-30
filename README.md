# duration-cli

A small, dependency-free tool that converts between human-readable
durations ("2h30m", "1d 4h", "90s") and total seconds — in either
direction, auto-detected from the input.

## Why

Converting "how many seconds is 2h30m" or "what's 9000 seconds in a
readable form" shouldn't need a search engine or a mental math session.
This does it in one command, and picks the right direction for you: a
bare number is seconds, anything with unit letters is a human duration.

## Install

```bash
pip install .
```

This installs a `duration-cli` command on your PATH.

## Usage

```bash
duration-cli 9000        # seconds -> human
duration-cli 2h30m       # human -> seconds
duration-cli "1d 4h"     # spaces are fine, quote if your shell needs it
duration-cli 90s
```

Example output:

```
$ duration-cli 9000
2h30m
$ duration-cli 2h30m
9000
```

### Supported units

| Unit | Meaning |
|------|---------|
| `s`  | seconds |
| `m`  | minutes |
| `h`  | hours   |
| `d`  | days    |
| `w`  | weeks   |

Units can be combined and written with or without spaces: `2h30m` and
`2h 30m` both parse to 9000 seconds.

### Exit codes

| Code | Meaning                                    |
|------|----------------------------------------------|
| 0    | Converted successfully                        |
| 2    | Input wasn't a valid duration or was a negative number of seconds |

## Development

```bash
pip install -e .
python -m unittest discover -s tests -v
```

## License

All rights reserved. This code is public for viewing and reference only —
no license is granted to use, copy, modify, or redistribute it. See
[LICENSE](LICENSE) for details.

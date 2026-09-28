#!/usr/bin/env python3
"""Filter `dconf dump` keyfile output, dropping excluded keys.

Keys are matched by their full path (e.g. /org/cinnamon/command-history)
against --exclude regexes. Sections left with no keys are dropped.

    dconf dump / | filter.py --exclude '^/org/cinnamon/command-history$'
"""

import argparse
import re
import sys


def parse_sections(lines):
    """Yield (header, [key lines]) for each [section] in a dconf keyfile."""
    header, keys = None, []
    for line in lines:
        line = line.rstrip("\n")
        if line.startswith("[") and line.endswith("]"):
            if header is not None:
                yield header, keys
            header, keys = line, []
        elif "=" in line and header is not None:
            keys.append(line)
    if header is not None:
        yield header, keys


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--exclude", action="append", default=[],
                        help="regex over the full key path (repeatable)")
    parser.add_argument("file", nargs="?", type=argparse.FileType("r"),
                        default=sys.stdin, help="keyfile to filter (default: stdin)")
    args = parser.parse_args()

    excludes = [re.compile(pattern) for pattern in args.exclude]

    sections = []
    for header, keys in parse_sections(args.file):
        section = header[1:-1]
        kept = [key for key in keys
                if not any(ex.search(f"/{section}/{key.split('=', 1)[0]}") for ex in excludes)]
        if kept:
            sections.append("\n".join([header] + kept))

    if sections:
        sys.stdout.write("\n\n".join(sections) + "\n")


if __name__ == "__main__":
    main()

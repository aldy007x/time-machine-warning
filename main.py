#!/usr/bin/env python3
"""Entry generator: Funniest Time Machine Warning Label.

Writes a single original warning-label line to $MAKEFUN_OUTPUT_DIR/entry.txt.
Deterministic, no network, no randomness, no external files.
"""

import os
import sys

ENTRY = "WARNING: Killing your own grandfather voids the warranty and may cancel the operator."


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(ENTRY + "\n")

    # Runtime self-check: read the file back and validate it.
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    non_blank = [line for line in lines if line.strip()]
    if len(non_blank) != 1:
        print(f"error: entry.txt must contain exactly one non-blank line, found {len(non_blank)}", file=sys.stderr)
        return 1
    line = non_blank[0]
    if not 1 <= len(line) <= 120:
        print(f"error: entry line is {len(line)} characters, must be 1-120", file=sys.stderr)
        return 1
    # The line must be exactly as written: no stray leading/trailing
    # whitespace, and the file must end with exactly one trailing newline.
    if line != line.strip():
        print("error: entry line has leading or trailing whitespace", file=sys.stderr)
        return 1
    if content != line + "\n":
        print("error: entry.txt must be exactly the entry line plus one newline", file=sys.stderr)
        return 1
    if line != ENTRY:
        print("error: entry.txt content does not match the intended entry", file=sys.stderr)
        return 1

    print(f"wrote {path} ({len(line)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

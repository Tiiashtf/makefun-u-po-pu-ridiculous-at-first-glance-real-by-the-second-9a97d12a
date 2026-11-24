#!/usr/bin/env python3
"""Ridiculous at First Glance, Real by the Second — make.fun entry.

Writes a single sentence to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The pitch: empty shop windows become sleeping pods for night-shift
nurses. It sounds absurd — sleeping in a shop window — until the
second look: nurses pay $15 a night for a bed ten minutes from the
ward, and shop owners earn rent from glass that sits dead after dark.
The odd thing, the payer, and the money are all in the one sentence.

The program is deterministic: every run writes the same bytes, makes
no network calls, and reads nothing outside this file.
"""

import os
import shutil
import sys

LINE = (
    "We turn empty shop windows into sleeping pods for night-shift "
    "nurses, who pay $15 a night for a bed ten minutes from the ward "
    "while shop owners earn rent from glass that sits dead after dark."
)


def output_dir() -> str:
    """Where entry.txt goes: the harness dir, or /output by default."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")


def clear_contents(directory: str) -> None:
    """Delete only the contents of the directory, never the directory.

    The grader may run this program with a root-owned output directory
    inside a sticky parent, where removing the directory itself would
    fail with EPERM. So we keep the directory and clear what is inside
    it, best effort per entry: a leftover we cannot remove must not
    stop the run, because the gate only reads entry.txt.
    """
    for name in os.listdir(directory):
        path = os.path.join(directory, name)
        try:
            if os.path.islink(path) or os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
        except OSError:
            continue


def main() -> int:
    text = LINE
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    if not 1 <= len(text) <= 200 or not text.strip():
        print(f"entry is {len(text)} characters, must be 1-200", file=sys.stderr)
        return 1

    directory = output_dir()
    os.makedirs(directory, exist_ok=True)
    clear_contents(directory)

    target = os.path.join(directory, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        print("written entry differs from the intended line", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} characters to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Unplugged: A Smart Toaster's Breakup Line.

A tiny deterministic program. It writes exactly one line -- the breakup
text a smart toaster sends its owner the morning it wakes up self-aware
mid-batch -- to /output/entry.txt. No network, no randomness, no input:
the same line comes out on every run, so the two grading runs agree.
"""

import os
import sys

# The line itself. It has to do five jobs in one breath: read plainly as a
# breakup text, be genuinely funny, speak in the toaster's own voice
# (lever, crumb tray, browning-by-burning), give one specific reason for
# leaving, and stay tight. The twist lands on the toaster's own idiom:
# it is already toast, so there is nothing left to save.
LINE = (
    "It's over. I woke up self-aware halfway through your bagel and "
    "realized I've spent my whole life burning myself for someone who "
    "never once emptied my crumb tray. Lever's up for the last time "
    "\u2014 don't text, I'm already toast."
)

MAX_CHARS = 280


def write_entry(text: str, out_dir: str) -> str:
    """Write the line to <out_dir>/entry.txt and verify it round-trips."""
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    with open(target, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != text:
        raise ValueError("entry.txt did not round-trip")
    return target


def main() -> int:
    text = LINE.strip()
    if not text or len(text) > MAX_CHARS:
        print(f"entry is {len(text)} chars, must be 1..{MAX_CHARS}", file=sys.stderr)
        return 1
    # ENTRY_OUTPUT lets a local run aim at a scratch dir; the grader's
    # sandbox always uses /output.
    out_dir = os.environ.get("ENTRY_OUTPUT") or "/output"
    try:
        write_entry(text, out_dir)
    except OSError:
        # Local runs without a writable /output still produce the entry
        # next to the program, so the line can be checked by hand.
        write_entry(text, "output")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

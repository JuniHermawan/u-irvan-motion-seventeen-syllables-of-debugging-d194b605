#!/usr/bin/env python3
"""Seventeen Syllables of Debugging — entry program.

Writes one haiku about debugging to /output/entry.txt
(or $MAKEFUN_OUTPUT_DIR/entry.txt when set).

The haiku (5-7-5, 73 characters, no trailing newline):

    read the error twice
    it blames the wrong line again
    I wrote that line too

Syllable counts, per word:
    read(1) the(1) error(2) twice(1) = 5
    it(1) blames(1) the(1) wrong(1) line(1) again(2) = 7
    I(1) wrote(1) that(1) line(1) too(1) = 5

Why this haiku: the picture is concrete and fresh (an error message that
points at the wrong line), and the last line reframes the blame — the
programmer, not the error, is at fault. No filler word is there just to
reach the count; it reads aloud like speech.

Stdlib only, no randomness, no time, no network: deterministic output.

Revision history:
    v1 (2026-11-24): first fresh write - haiku constant + 5-7-5 self-check.
    v2 (2026-11-24): added the trailing-whitespace / trailing-newline
        gate below; the entry must end exactly at the last word, with no
        trailing newline, so the byte count stays at 73 (the exact-tie
        break favours the smaller text).
"""

import os

HAIKU = (
    "read the error twice\n"
    "it blames the wrong line again\n"
    "I wrote that line too"
)

# Expected shape of the entry, checked by _self_check() before writing.
EXPECTED_LINES = 3
EXPECTED_SYLLABLES = (5, 7, 5)
MAX_CHARS = 200

# Small hand-counted syllable table for the words this haiku uses.
# Kept explicit so the self-check counts the actual words, not a guess.
_SYLLABLES = {
    "read": 1, "the": 1, "error": 2, "twice": 1,
    "it": 1, "blames": 1, "wrong": 1, "line": 1, "again": 2,
    "i": 1, "wrote": 1, "that": 1, "too": 1,
}


def _count_syllables(line):
    total = 0
    for word in line.split():
        total += _SYLLABLES[word.strip(".,;:!?").lower()]
    return total


def _self_check(text):
    """Gate: 3 lines, 5-7-5 syllables, 1-200 chars, UTF-8, non-whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    text.encode("utf-8")  # raises if not encodable as UTF-8
    if not 1 <= len(text) <= MAX_CHARS:
        raise ValueError("entry must be 1-%d characters, got %d"
                         % (MAX_CHARS, len(text)))
    if text != text.rstrip():
        raise ValueError("entry must not end with trailing whitespace "
                         "or a trailing newline")
    for line in text.split("\n"):
        if line != line.rstrip():
            raise ValueError("line %r has trailing whitespace" % line)
    lines = text.split("\n")
    if len(lines) != EXPECTED_LINES:
        raise ValueError("entry must have %d lines, got %d"
                         % (EXPECTED_LINES, len(lines)))
    for line, expected in zip(lines, EXPECTED_SYLLABLES):
        got = _count_syllables(line)
        if got != expected:
            raise ValueError("line %r has %d syllables, expected %d"
                             % (line, got, expected))


def main():
    _self_check(HAIKU)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(HAIKU)


if __name__ == "__main__":
    main()

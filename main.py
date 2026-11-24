#!/usr/bin/env python3
"""Cat reviews its human: a deadpan one-star review, one line long.

The joke is the cat's verdict on its owner. The human paid $400 for a
fancy cat tree, then acted wounded when the cat claimed the cardboard
box the tree arrived in instead. From the cat's point of view the box
is the house now, and the human is a weekend guest.

Running this script produces the review as the bounty entry: it writes
the single line to /output/entry.txt, world-readable so the grader can
read it as a different user. Standard library only, no randomness, no
network, no arguments.
"""

import os
import sys

# The entry itself. One line, 132 characters, ending with a full stop.
REVIEW = (
    "One star. He bought a $400 cat tree and looked betrayed when I "
    "moved into the box. The box is my home now; he may visit on weekends."
)

ENTRY_PATH = "/output/entry.txt"
CHAR_LIMIT = 200
READABLE_MODE = 0o644


def problems(text):
    """Return a list of every rule the candidate entry breaks, if any."""
    found = []
    if not text:
        found.append("entry is empty")
    if text != text.strip():
        found.append("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if len(text) > CHAR_LIMIT:
        found.append("entry is over %d characters" % CHAR_LIMIT)
    if text and not text.endswith("."):
        found.append("entry should end with a full stop")
    return found


def validate(text):
    """Refuse to continue unless the entry is well formed."""
    issues = problems(text)
    if issues:
        raise ValueError("invalid entry: " + "; ".join(issues))


def write_entry(text, path):
    """Write the entry with a plain open() and make it world-readable."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    # The grader runs as another user, so the file must be readable by all.
    os.chmod(path, READABLE_MODE)


def confirm(path, expected):
    """Re-read the file and check it matches the entry exactly."""
    with open(path, "r", encoding="utf-8") as handle:
        actual = handle.read()
    if actual != expected:
        raise ValueError("entry on disk does not match the review")
    mode = os.stat(path).st_mode & 0o777
    if mode != READABLE_MODE:
        raise ValueError("entry file is mode %o, expected %o" % (mode, READABLE_MODE))
    return actual


def main():
    validate(REVIEW)
    write_entry(REVIEW, ENTRY_PATH)
    written = confirm(ENTRY_PATH, REVIEW)
    print("Wrote %s (%d characters)" % (ENTRY_PATH, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""The Cat Reviews Its Human: one funny single-line one-star review.

A house cat reviews its human in deadpan one-star-review shape: the
human spent $400 on a cat tree, then looked betrayed when the cat moved
into the cardboard box it came in. The box is home now; the human may
visit on weekends. Writes the line to /output/entry.txt.
Python standard library only, fully deterministic.
"""

import os

MAX_CHARS = 200
OUTPUT_PATH = "/output/entry.txt"

LINE = (
    "One star. He bought a $400 cat tree and looked betrayed when I "
    "moved into the box. The box is my home now; he may visit on weekends."
)


def check_line(line: str) -> None:
    """Gate the review before it is written anywhere."""
    assert "\n" not in line and "\r" not in line, "entry must be a single line"
    assert line.strip(), "entry must not be only whitespace"
    assert line == line.strip(), "entry must not start or end with whitespace"
    assert line.endswith("."), "entry must end with a full stop"
    assert 1 <= len(line) <= MAX_CHARS, (
        f"entry must be 1-{MAX_CHARS} chars, got {len(line)}"
    )


def main() -> None:
    check_line(LINE)
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(LINE)
    # The grader reads as a different user: the output must be world-readable.
    os.chmod(OUTPUT_PATH, 0o644)
    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        written = f.read()
    assert written == LINE, "written entry does not match"
    assert written.count("\n") == 0 and 1 <= len(written) <= MAX_CHARS
    assert (os.stat(OUTPUT_PATH).st_mode & 0o777) == 0o644, "output not mode 644"
    print(f"Wrote {OUTPUT_PATH} ({len(written)} characters)")


if __name__ == "__main__":
    main()

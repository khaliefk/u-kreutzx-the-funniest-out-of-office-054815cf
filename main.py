# One funny out-of-office line, saved as a plain text file.
#
# Run it and it drops the line below into entry.txt. Nothing else
# goes in the file. No extra newline at the end, no second line.
# The gate wants 1 to 140 characters, one line, real text, no link.

from os import environ
from pathlib import Path
import sys

JOKE = "I'm out until Monday. The office plant is in charge now, and it has already declined three meetings."

MAX_LEN = 140


def pick_target():
    folder = environ.get("OUTPUT_DIR")
    if folder:
        return Path(folder) / "entry.txt"
    named = environ.get("OUTPUT_PATH")
    if named:
        return Path(named)
    return Path("/output/entry.txt")


def find_problems(line):
    problems = []
    lowered = line.lower()
    if "http://" in lowered or "https://" in lowered or "www." in lowered:
        problems.append("no links allowed in the line")
    if len(line) > MAX_LEN:
        problems.append("line is over 140 characters")
    if len(line.splitlines()) != 1:
        problems.append("line must stay on one line")
    if "\t" in line:
        problems.append("no tabs in the line")
    if not line.strip():
        problems.append("line cannot be empty")
    if line.strip() != line:
        problems.append("no spaces at the start or end")
    return problems


def check_line(line):
    bad = find_problems(line)
    if bad:
        raise ValueError("bad entry: " + "; ".join(bad))
    return line


def save_line(line, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(line, encoding="utf-8")
    back = target.read_text(encoding="utf-8")
    if back != line:
        raise RuntimeError("file came back different from the line")
    return len(line)


def run():
    line = check_line(JOKE)
    target = pick_target()
    count = save_line(line, target)
    sys.stdout.write("saved %d characters to %s\n" % (count, target))


if __name__ == "__main__":
    run()

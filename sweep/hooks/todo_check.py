#!/usr/bin/env python3
"""Git pre-commit check: every new TODO or FIXME names a ticket.

A TODO without a ticket can't be proven stale later, so agents treat it as a
live task forever. Only lines added in the staged diff are checked.
"""
import re
import subprocess
import sys

MARKER = re.compile(r"\b(TODO|FIXME)\b")
TICKET = re.compile(r"#\d+|bug/\d+|\b[A-Z][A-Z0-9]+-\d+\b|\bCSC[a-z]{2}\d{5}\b|https?://\S+")


def main():
    diff = subprocess.run(
        ["git", "diff", "--cached", "-U0", "--no-color"], capture_output=True, text=True, check=True
    ).stdout
    path, bad = "", []
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("+") and MARKER.search(line) and not TICKET.search(line):
            bad.append(f"{path}: {line[1:].strip()}")
    if bad:
        print("New TODO/FIXME without a ticket ID (#123, PROJ-42, CSCab12345, or a URL):", file=sys.stderr)
        print("\n".join(bad), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

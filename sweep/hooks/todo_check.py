#!/usr/bin/env python3
"""Every new TODO or FIXME names a ticket.

A TODO without a ticket can't be proven stale later, so agents treat it as a
live task forever. Only added lines are checked. Existing TODOs pass.

  todo_check.py          git pre-commit: check lines added in the staged diff
  todo_check.py --hook   Claude Code PreToolUse hook on Edit|Write|MultiEdit:
                         exit 2 blocks the edit, so the agent fixes it at once
"""
from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys

MARKER = re.compile(r"\b(TODO|FIXME)\b")
TICKET = re.compile(
    r"#\d+|bug/\d+|\b[A-Z][A-Z0-9]+-\d+\b|\bCSC[a-z]{2}\d{5}\b|https?://\S+"
    # Beads IDs (tasks-orf, tasks-orf.2) only inside parens: TODO(tasks-orf).
    r"|\(\s*[a-z][a-z0-9]*-[a-z0-9]+(?:\.\d+)*\s*\)"
)
CODE_SPAN = re.compile(r"`[^`]*`")  # `TODO` in docs is prose, not a task.
HOOK_TOOLS = {"Edit", "Write", "MultiEdit"}
MSG = "New TODO/FIXME without a ticket ID (#123, PROJ-42, CSCab12345, TODO(tasks-abc), or a URL):"


def is_bare(line):
    line = CODE_SPAN.sub("", line)
    return bool(MARKER.search(line)) and not TICKET.search(line)


def added_lines(old, new):
    """Lines in new that old does not already have, so moving a TODO is not new."""
    have = Counter(old.splitlines())
    out = []
    for line in new.splitlines():
        if have[line]:
            have[line] -= 1
        else:
            out.append(line)
    return out


def hook_bad(event):
    tool = event.get("tool_name", "")
    inp = event.get("tool_input") or {}
    if tool not in HOOK_TOOLS:
        return []
    path = inp.get("file_path", "")
    if tool == "Write":
        try:
            old = Path(path).read_text()
        except (OSError, UnicodeDecodeError):
            old = ""
        pairs = [(old, inp.get("content", ""))]
    elif tool == "Edit":
        pairs = [(inp.get("old_string", ""), inp.get("new_string", ""))]
    else:
        pairs = [(e.get("old_string", ""), e.get("new_string", "")) for e in inp.get("edits", [])]
    return [f"{path}: {l.strip()}" for old, new in pairs for l in added_lines(old, new) if is_bare(l)]


def staged_bad():
    diff = subprocess.run(
        ["git", "diff", "--cached", "-U0", "--no-color"], capture_output=True, text=True, check=True
    ).stdout
    path, bad = "", []
    for line in diff.splitlines():
        if line.startswith("+++ "):
            path = line[6:] if line.startswith("+++ b/") else line[4:]
        elif line.startswith("+") and is_bare(line[1:]):
            bad.append(f"{path}: {line[1:].strip()}")
    return bad


def main():
    if "--hook" in sys.argv[1:]:
        try:
            bad = hook_bad(json.load(sys.stdin))
        except json.JSONDecodeError:
            return  # Never block on input we can't read.
        code = 2
    else:
        bad, code = staged_bad(), 1
    if bad:
        print(MSG, file=sys.stderr)
        print("\n".join(bad), file=sys.stderr)
        print("File a ticket first, or drop the TODO.", file=sys.stderr)
        sys.exit(code)


if __name__ == "__main__":
    main()

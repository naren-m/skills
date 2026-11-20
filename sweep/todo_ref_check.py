#!/usr/bin/env python3
"""Block new TODO/FIXME comments that do not name an issue.

A TODO with an issue ID can be proven stale later: close the issue and the
comment is dead. A bare TODO cannot. This check keeps new TODOs provable.

Modes:
  --hook    Claude Code PreToolUse hook. Reads the tool call JSON on stdin.
            Exit 2 blocks the edit and sends the reason back to the agent.
  --staged  git pre-commit hook. Checks lines added in the staged diff.

Accepted refs: TODO(#123), TODO(bug/123), TODO(PROJ-42), TODO(tasks-orf.2),
TODO(https://...). Override with the SWEEP_TODO_REF_REGEX environment variable.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

DEFAULT_REF = r"#\d+|bug/\d+|[A-Za-z][\w.]*-[\w.]+|https?://\S+"
# Only comment-shaped TODOs count. Prose that mentions `TODO` is not a task.
COMMENT_TODO = re.compile(r"(?:#|//|/\*|\*|--|<!--|;)\s*(TODO|FIXME)\b(.*)")


def ref_pattern():
    ref = os.environ.get("SWEEP_TODO_REF_REGEX", DEFAULT_REF)
    return re.compile(r"^\(\s*(?:" + ref + r")\s*\)")


def bare_todos(text):
    """Return lines in text whose TODO/FIXME comment names no issue."""
    ref = ref_pattern()
    bad = []
    for line in text.splitlines():
        m = COMMENT_TODO.search(line)
        if m and not ref.match(m.group(2).lstrip(":").lstrip()):
            bad.append(line.strip())
    return bad


def added_bare_todos(old, new):
    """Bare TODO lines in new that old does not already have."""
    seen = {}
    for line in bare_todos(old):
        seen[line] = seen.get(line, 0) + 1
    added = []
    for line in bare_todos(new):
        if seen.get(line, 0):
            seen[line] -= 1
        else:
            added.append(line)
    return added


def hook_findings(event):
    tool = event.get("tool_name", "")
    inp = event.get("tool_input", {}) or {}
    if tool == "Write":
        path = Path(inp.get("file_path", ""))
        try:
            old = path.read_text() if path.is_file() else ""
        except (OSError, UnicodeDecodeError):
            old = ""
        return added_bare_todos(old, inp.get("content", ""))
    if tool == "Edit":
        return added_bare_todos(inp.get("old_string", ""), inp.get("new_string", ""))
    if tool == "MultiEdit":
        found = []
        for e in inp.get("edits", []):
            found += added_bare_todos(e.get("old_string", ""), e.get("new_string", ""))
        return found
    return []


def staged_findings():
    diff = subprocess.run(
        ["git", "diff", "--cached", "-U0", "--no-color"],
        capture_output=True, text=True, check=True,
    ).stdout
    added = [l[1:] for l in diff.splitlines() if l.startswith("+") and not l.startswith("+++")]
    return bare_todos("\n".join(added))


def report(found):
    lines = "\n".join(f"  {l}" for l in found[:10])
    return (
        "New TODO/FIXME without an issue ID:\n"
        f"{lines}\n"
        "Name the issue, for example TODO(#123) or TODO(tasks-abc). "
        "Without an ID, nobody can prove the TODO is stale later. "
        "If no issue exists, file one first or drop the TODO."
    )


def main(argv):
    if "--hook" in argv:
        try:
            event = json.load(sys.stdin)
        except json.JSONDecodeError:
            return 0  # Never block on input we cannot read.
        found = hook_findings(event)
        if found:
            print(report(found), file=sys.stderr)
            return 2
        return 0
    if "--staged" in argv:
        found = staged_findings()
        if found:
            print(report(found), file=sys.stderr)
            return 1
        return 0
    print(__doc__, file=sys.stderr)
    return 64


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

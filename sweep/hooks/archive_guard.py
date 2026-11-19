#!/usr/bin/env python3
"""Block agent reads of archive/ so archived plans stay out of context.

Runs as a preToolUse hook in Cursor and a PreToolUse hook in Claude Code.
Writes into archive/ stay allowed so sweep's Apply step can move files there.
"""
import json
import re
import sys

READ_TOOLS = {"Read", "Grep", "Glob", "LS", "Edit", "MultiEdit", "StrReplace", "NotebookRead", "NotebookEdit"}
SHELL_TOOLS = {"Bash", "Shell"}
SHELL_ALLOWED = ("git mv ", "git add ", "git status", "mkdir ")
# ponytail: matches any path segment named archive, not only the repo root one.
# Scope it with the hook's cwd if a project has an unrelated archive/ directory.
ARCHIVE = re.compile(r"(?:^|[\s\"'=:/(])archive(?:/|\s|$)")
REASON = "archive/ holds retired plans and notes. Don't read it unless the user asks."


def touches_archive(tool, tool_input):
    if tool in SHELL_TOOLS:
        command = tool_input.get("command", "").strip()
        return not command.startswith(SHELL_ALLOWED) and bool(ARCHIVE.search(command))
    if tool in READ_TOOLS:
        # Grep's pattern is search text, not a path.
        values = [v for k, v in tool_input.items() if isinstance(v, str) and not (tool == "Grep" and k == "pattern")]
        return any(ARCHIVE.search(v) for v in values)
    return False


def main():
    event = json.load(sys.stdin)
    blocked = touches_archive(event.get("tool_name", ""), event.get("tool_input") or {})
    if event.get("hook_event_name") == "PreToolUse":
        if blocked:
            print(REASON, file=sys.stderr)
            sys.exit(2)
        return
    if blocked:
        print(json.dumps({"permission": "deny", "user_message": REASON, "agent_message": REASON}))
    else:
        print(json.dumps({"permission": "allow"}))


if __name__ == "__main__":
    main()

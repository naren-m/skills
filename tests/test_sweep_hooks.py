import json
from pathlib import Path
import subprocess
import sys

import pytest

HOOKS = Path(__file__).resolve().parents[1] / "sweep" / "hooks"
GUARD = HOOKS / "archive_guard.py"
TODO_CHECK = HOOKS / "todo_check.py"


def run_guard(event):
    return subprocess.run(
        [sys.executable, str(GUARD)], input=json.dumps(event), capture_output=True, text=True
    )


@pytest.mark.parametrize(
    "tool, tool_input, blocked",
    [
        ("Read", {"file_path": "archive/old-plan.md"}, True),
        ("Read", {"file_path": "/repo/archive/old-plan.md"}, True),
        ("Read", {"file_path": "src/app.py"}, False),
        ("Read", {"file_path": "src/myarchive/app.py"}, False),
        ("Grep", {"pattern": "archive", "path": "src"}, False),
        ("Grep", {"pattern": "login", "path": "archive"}, True),
        ("Glob", {"pattern": "archive/**/*.md"}, True),
        ("Bash", {"command": "cat archive/old-plan.md"}, True),
        ("Bash", {"command": "rg login archive"}, True),
        ("Bash", {"command": "git mv specs/login.md archive/login.md"}, False),
        ("Bash", {"command": "mkdir -p archive"}, False),
        ("Write", {"file_path": "archive/login-section.md", "content": "x"}, False),
    ],
)
def test_claude_code_archive_guard(tool, tool_input, blocked):
    result = run_guard({"hook_event_name": "PreToolUse", "tool_name": tool, "tool_input": tool_input})

    assert (result.returncode == 2) == blocked
    assert ("archive/" in result.stderr) == blocked


@pytest.mark.parametrize(
    "tool, tool_input, permission",
    [
        ("Read", {"file_path": "/repo/archive/old-plan.md"}, "deny"),
        ("Shell", {"command": "head archive/old-plan.md"}, "deny"),
        ("Read", {"file_path": "/repo/src/app.py"}, "allow"),
    ],
)
def test_cursor_archive_guard(tool, tool_input, permission):
    result = run_guard({"hook_event_name": "preToolUse", "tool_name": tool, "tool_input": tool_input})

    assert result.returncode == 0
    assert json.loads(result.stdout)["permission"] == permission


@pytest.mark.parametrize(
    "line, passes",
    [
        ("# TODO fix the retry loop", False),
        ("// FIXME: flaky", False),
        ("# TODO(#12): drop after migration", True),
        ("# TODO(bug/123): remove shim", True),
        ("// FIXME(PROJ-42) handle empty list", True),
        ("# TODO(CSCab12345) remove workaround", True),
        ("# TODO https://github.com/o/r/issues/7", True),
        ("todo_items = []", True),
    ],
)
def test_todo_check_requires_ticket_id_on_new_todos(tmp_path, line, passes):
    git = ["git", "-C", str(tmp_path)]
    subprocess.run(git + ["init", "-q"], check=True)
    (tmp_path / "app.py").write_text(line + "\n")
    subprocess.run(git + ["add", "app.py"], check=True)

    result = subprocess.run(
        [sys.executable, str(TODO_CHECK)], cwd=tmp_path, capture_output=True, text=True
    )

    assert (result.returncode == 0) == passes

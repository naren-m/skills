import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import subprocess

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "sweep" / "todo_ref_check.py"
loader = importlib.machinery.SourceFileLoader("todo_ref_check", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
check = importlib.util.module_from_spec(spec)
loader.exec_module(check)


@pytest.mark.parametrize(
    "line,bare",
    [
        ("# TODO(#123): drop shim", False),
        ("// TODO(bug/456) remove", False),
        ("/* FIXME(PROJ-42) */", False),
        ("# TODO(tasks-orf.2) final token", False),
        ("-- TODO(https://github.com/o/r/issues/9)", False),
        ("# TODO: clean this up", True),
        ("// FIXME later", True),
        ("# TODO(naren) ask", True),
        ("<!-- TODO add section -->", True),
        ("- `TODO` and `FIXME` comments", False),  # prose, not a comment
        ("x = 'TODO'", False),
    ],
)
def test_bare_todos(line, bare):
    assert bool(check.bare_todos(line)) == bare


@pytest.mark.parametrize(
    "event,blocked",
    [
        ({"tool_name": "Edit", "tool_input": {"old_string": "a", "new_string": "a\n# TODO: x"}}, True),
        ({"tool_name": "Edit", "tool_input": {"old_string": "a", "new_string": "a\n# TODO(#1): x"}}, False),
        # Moving an existing bare TODO is not a new one.
        ({"tool_name": "Edit", "tool_input": {"old_string": "# TODO: x\na", "new_string": "a\n# TODO: x"}}, False),
        ({"tool_name": "MultiEdit", "tool_input": {"edits": [{"old_string": "a", "new_string": "// FIXME y"}]}}, True),
        ({"tool_name": "Write", "tool_input": {"file_path": "/nonexistent/f.py", "content": "# TODO: z"}}, True),
        ({"tool_name": "Bash", "tool_input": {"command": "echo '# TODO: z'"}}, False),
    ],
)
def test_hook_mode(event, blocked, monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", io.StringIO(json.dumps(event)))
    assert check.main(["--hook"]) == (2 if blocked else 0)
    assert ("issue ID" in capsys.readouterr().err) == blocked


def test_hook_mode_ignores_bad_json(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("not json"))
    assert check.main(["--hook"]) == 0


def test_write_keeps_existing_bare_todos(tmp_path):
    f = tmp_path / "f.py"
    f.write_text("# TODO: old\n")
    event = {"tool_name": "Write", "tool_input": {"file_path": str(f), "content": "# TODO: old\nx = 1\n"}}
    assert check.hook_findings(event) == []


def test_ref_regex_override(monkeypatch):
    monkeypatch.setenv("SWEEP_TODO_REF_REGEX", r"JIRA-\d+")
    assert check.bare_todos("# TODO(#1)")
    assert not check.bare_todos("# TODO(JIRA-7)")


def test_staged_mode(tmp_path, monkeypatch):
    git = lambda *a: subprocess.run(["git", *a], cwd=tmp_path, check=True, capture_output=True)
    git("init", "-q")
    (tmp_path / "a.py").write_text("# TODO: old\n")
    git("add", "a.py")
    git("-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "init")
    monkeypatch.chdir(tmp_path)
    assert check.main(["--staged"]) == 0
    (tmp_path / "a.py").write_text("# TODO: old\n# TODO(#2): ok\n")
    git("add", "a.py")
    assert check.main(["--staged"]) == 0
    (tmp_path / "a.py").write_text("# TODO: old\n# FIXME: new\n")
    git("add", "a.py")
    assert check.main(["--staged"]) == 1

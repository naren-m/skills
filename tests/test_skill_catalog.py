import importlib.machinery
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
from unittest import mock

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "bin" / "skill-catalog"
loader = importlib.machinery.SourceFileLoader("skill_catalog", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
catalog = importlib.util.module_from_spec(spec)
loader.exec_module(catalog)


def test_install_and_update_preserves_local_edits(tmp_path):
    origin = tmp_path / "origin"
    skill = origin / "skills" / "demo"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("original")
    (skill / "reference.md").write_text("reference")
    entry = {"name": "demo", "url": "https://github.com/a/b/tree/main/skills/demo"}
    dest = tmp_path / "installed"

    def run(command, **kwargs):
        if "clone" in command:
            shutil.copytree(origin, Path(command[-1]))
        return subprocess.CompletedProcess(command, 0)

    with mock.patch.object(catalog.subprocess, "run", side_effect=run), mock.patch.object(
        catalog.subprocess, "check_output", return_value="a" * 40 + "\n"
    ):
        catalog.install(entry, dest)
        target = dest / "demo"
        assert (target / "reference.md").read_text() == "reference"
        assert json.loads((target / catalog.MARKER).read_text())["commit"] == "a" * 40
        with pytest.raises(ValueError, match="already exists"):
            catalog.install(entry, dest)
        (skill / "SKILL.md").write_text("updated")
        catalog.install(entry, dest, update=True)
        assert (target / "SKILL.md").read_text() == "updated"
        (target / "SKILL.md").write_text("local edit")
        with pytest.raises(ValueError, match="local changes"):
            catalog.install(entry, dest, update=True)
        assert (target / "SKILL.md").read_text() == "local edit"


def test_url_validation():
    assert catalog.parse_url("https://github.com/a/b/tree/main/skills/demo") == (
        "https://github.com/a/b.git", "main", "skills/demo"
    )
    with pytest.raises(ValueError):
        catalog.parse_url("https://github.com/a/b/tree/main/../demo")

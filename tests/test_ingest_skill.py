import importlib.machinery
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "ingest-skill" / "ingest_skill.py"
loader = importlib.machinery.SourceFileLoader("ingest_skill", str(SCRIPT))
spec = importlib.util.spec_from_loader(loader.name, loader)
ingest = importlib.util.module_from_spec(spec)
loader.exec_module(ingest)


@pytest.mark.parametrize(
    "raw,url,name",
    [
        (
            "https://github.com/cursor/plugins/blob/main/pstack/skills/statechart/SKILL.md",
            "https://github.com/cursor/plugins/tree/main/pstack/skills/statechart",
            "statechart",
        ),
        (
            "https://github.com/cursor/plugins/blob/main/pstack/skills/statechart/SKILL",
            "https://github.com/cursor/plugins/tree/main/pstack/skills/statechart",
            "statechart",
        ),
        (
            "https://github.com/naren-m/skills/tree/main/sutra-writing",
            "https://github.com/naren-m/skills/tree/main/sutra-writing",
            "sutra-writing",
        ),
    ],
)
def test_github_skill_url_becomes_catalog_tree_url(raw, url, name):
    assert ingest.skill_url(raw) == (url, name)


def test_skill_url_rejects_non_skill_blob():
    with pytest.raises(ValueError):
        ingest.skill_url("https://github.com/a/b/blob/main/README.md")


def test_catalog_paths():
    personal = ingest.catalog("personal")
    work = ingest.catalog("work")
    assert personal.checkout == Path("/data/hdd/naren-m-skills")
    assert personal.owner_repo == "naren-m/skills"
    assert work.checkout == Path("/data/hdd/skills")
    assert work.owner_repo == "nmudivar_cisco/skills"
    with pytest.raises(ValueError):
        ingest.catalog("other")


def test_missing_checkout_is_cloned(tmp_path, monkeypatch):
    checkout = tmp_path / "skills"
    spec = ingest.Catalog(
        "personal",
        checkout,
        "https://github.com/naren-m/skills.git",
        "naren-m/skills",
    )

    real_run = subprocess.run

    def run(cmd, **kwargs):
        if cmd[:3] == ["git", "clone", spec.clone_url]:
            real_run(["git", "init", "-q", cmd[-1]], check=True)
            real_run(["git", "-C", cmd[-1], "remote", "add", "origin", spec.clone_url], check=True)
            return subprocess.CompletedProcess(cmd, 0)
        return real_run(cmd, **kwargs)

    monkeypatch.setattr(ingest.subprocess, "run", run)
    ingest.ensure_checkout(spec)
    assert (checkout / ".git").exists()


def test_prepare_refuses_a_dirty_checkout(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    (repo / "skill-catalog.json").write_text("{}\n")
    _git(repo, "add", "skill-catalog.json")
    _git(repo, "commit", "-q", "-m", "init")
    (repo / "skill-catalog.json").write_text('{"skills": []}\n')
    with pytest.raises(ValueError, match="uncommitted"):
        ingest.prepare(repo)


def test_wrong_origin_is_refused(tmp_path):
    checkout = tmp_path / "skills"
    subprocess.run(["git", "init", "-q", str(checkout)], check=True)
    subprocess.run(
        ["git", "-C", str(checkout), "remote", "add", "origin", "https://github.com/other/skills.git"],
        check=True,
    )
    spec = ingest.Catalog("work", checkout, "git@github.com:nmudivar_cisco/skills.git", "nmudivar_cisco/skills")
    with pytest.raises(ValueError, match="nmudivar_cisco/skills"):
        ingest.ensure_checkout(spec)


def test_add_entry_is_idempotent_and_refuses_a_different_url(tmp_path):
    catalog_path = tmp_path / "skill-catalog.json"
    catalog_path.write_text('{"skills": []}\n')
    url = "https://github.com/cursor/plugins/tree/main/pstack/skills/statechart"
    ingest.add_entry(catalog_path, "statechart", url)
    ingest.add_entry(catalog_path, "statechart", url)
    assert json.loads(catalog_path.read_text())["skills"] == [{"name": "statechart", "url": url}]
    with pytest.raises(ValueError, match="statechart"):
        ingest.add_entry(catalog_path, "statechart", url + "-other")


def test_install_clones_once_and_links_the_other_dirs(tmp_path, monkeypatch):
    checkout = tmp_path / "repo"
    (checkout / "bin").mkdir(parents=True)
    calls = []

    def run(cmd, **kwargs):
        calls.append(cmd)
        installed = Path(cmd[-1]) / "statechart"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("skill")
        return subprocess.CompletedProcess(cmd, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr(ingest.subprocess, "run", run)
    dests = [tmp_path / "cursor", tmp_path / "codex"]
    failed = ingest.install_host(checkout, "statechart", dests)
    assert failed == []
    assert len(calls) == 1
    assert calls[0][-1] == str(dests[0])
    link = dests[1] / "statechart"
    assert link.is_symlink()
    assert link.resolve() == (dests[0] / "statechart").resolve()


def test_install_leaves_an_existing_skill_directory(tmp_path, monkeypatch):
    checkout = tmp_path / "repo"
    (checkout / "bin").mkdir(parents=True)
    kept = tmp_path / "codex" / "statechart"
    kept.mkdir(parents=True)
    (kept / "SKILL.md").write_text("local")

    def run(cmd, **kwargs):
        installed = Path(cmd[-1]) / "statechart"
        installed.mkdir(parents=True)
        (installed / "SKILL.md").write_text("skill")
        return subprocess.CompletedProcess(cmd, 0, stdout="ok\n", stderr="")

    monkeypatch.setattr(ingest.subprocess, "run", run)
    failed = ingest.install_host(checkout, "statechart", [tmp_path / "cursor", tmp_path / "codex"])
    assert failed == []
    assert not kept.is_symlink()
    assert (kept / "SKILL.md").read_text() == "local"


def _git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True)


def test_publish_commits_and_pushes_only_the_catalog(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    (repo / "skill-catalog.json").write_text('{"skills": []}\n')
    (repo / "README.md").write_text("keep\n")
    _git(repo, "add", "skill-catalog.json", "README.md")
    _git(repo, "commit", "-q", "-m", "init")
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    _git(repo, "remote", "add", "origin", str(remote))
    _git(repo, "push", "-q", "-u", "origin", "HEAD")
    (repo / "skill-catalog.json").write_text('{"skills": [{"name": "statechart", "url": "https://github.com/a/b/tree/main/statechart"}]}\n')
    (repo / "README.md").write_text("dirty\n")
    pushed = []

    real_run = subprocess.run

    def run(cmd, **kwargs):
        if cmd[:3] == ["git", "-C", str(repo)] and "push" in cmd:
            pushed.append(cmd)
            return real_run(["git", "-C", str(repo), "push", "-q", "origin", "HEAD"], check=True)
        return real_run(cmd, **kwargs)

    monkeypatch.setattr(ingest.subprocess, "run", run)
    assert ingest.publish(repo, "Catalog statechart.") == "pushed"
    assert pushed
    message = subprocess.check_output(["git", "-C", str(repo), "log", "-1", "--format=%s"], text=True)
    assert "Catalog statechart." in message
    dirty = subprocess.check_output(["git", "-C", str(repo), "status", "--porcelain"], text=True)
    assert "README.md" in dirty
    assert "skill-catalog.json" not in dirty


def test_publish_uses_the_given_remote_header(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "test@example.com")
    _git(repo, "config", "user.name", "test")
    (repo / "skill-catalog.json").write_text('{"skills": []}\n')
    _git(repo, "add", "skill-catalog.json")
    _git(repo, "commit", "-q", "-m", "init")
    (repo / "skill-catalog.json").write_text('{"skills": [{"name": "statechart", "url": "https://github.com/a/b/tree/main/statechart"}]}\n')
    calls = []
    real_run = subprocess.run

    def run(cmd, **kwargs):
        if "push" in cmd:
            calls.append((cmd, kwargs.get("env") or {}))
            return subprocess.CompletedProcess(cmd, 0)
        return real_run(cmd, **kwargs)

    monkeypatch.setattr(ingest.subprocess, "run", run)
    assert ingest.publish(
        repo,
        "Catalog statechart.",
        push_token="secret",
        push_remote="https://github.com/naren-m/skills.git",
    ) == "pushed"
    cmd, env = calls[0]
    assert "secret" not in cmd
    assert env["GH_TOKEN"] == "secret"
    assert cmd[3:5] == ["-c", "credential.helper="]
    assert cmd[-2:] == ["https://github.com/naren-m/skills.git", "HEAD:main"]

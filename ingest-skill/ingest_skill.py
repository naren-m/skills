#!/usr/bin/env python3
"""Add a GitHub skill URL to the personal or work catalog and install it."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlparse

HOST_DESTS = (
    Path.home() / ".cursor/skills",
    Path.home() / ".codex/skills",
    Path.home() / ".agents/skills",
)


class Catalog:
    def __init__(self, name, checkout, clone_url, owner_repo):
        self.name = name
        self.checkout = Path(checkout)
        self.clone_url = clone_url
        self.owner_repo = owner_repo


def catalog(name):
    if name == "personal":
        return Catalog(
            name,
            Path("/data/hdd/naren-m-skills"),
            "https://github.com/naren-m/skills.git",
            "naren-m/skills",
        )
    if name == "work":
        return Catalog(
            name,
            Path("/data/hdd/skills"),
            "git@github.com:nmudivar_cisco/skills.git",
            "nmudivar_cisco/skills",
        )
    raise ValueError(f"Catalog must be personal or work, not {name}")


def owner_repo(remote):
    remote = remote.strip()
    if remote.endswith(".git"):
        remote = remote[:-4]
    if remote.startswith("git@github.com:"):
        return remote.split(":", 1)[1]
    if remote.startswith("ssh://git@github.com/"):
        return remote.split("github.com/", 1)[1]
    parsed = urlparse(remote)
    if parsed.netloc == "github.com":
        return parsed.path.strip("/")
    raise ValueError(f"Unrecognized Git origin: {remote}")


def skill_url(raw):
    parsed = urlparse(raw)
    parts = [p for p in parsed.path.split("/") if p]
    if (
        parsed.scheme != "https"
        or parsed.netloc != "github.com"
        or parsed.query
        or parsed.fragment
        or len(parts) < 5
        or parts[2] not in ("tree", "blob")
    ):
        raise ValueError("Expected a https://github.com/OWNER/REPO/tree|blob/REF/... URL")
    owner, repo, kind, ref, *path = parts
    if kind == "blob":
        if path[-1] not in ("SKILL.md", "SKILL"):
            raise ValueError("A blob URL must point at SKILL.md")
        path = path[:-1]
    if not path or any(p in (".", "..") for p in (owner, repo, ref, *path)):
        raise ValueError("URL has an invalid skill path")
    if not all(re.fullmatch(r"[A-Za-z0-9_.-]+", p) for p in (owner, repo, ref, *path)):
        raise ValueError("URL has unsupported path characters")
    name = path[-1]
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_.-]*", name):
        raise ValueError(f"Invalid skill name: {name}")
    return f"https://github.com/{owner}/{repo}/tree/{ref}/{'/'.join(path)}", name


def ensure_checkout(spec):
    if not spec.checkout.exists():
        spec.checkout.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "clone", spec.clone_url, str(spec.checkout)], check=True)
    remote = subprocess.check_output(
        ["git", "-C", str(spec.checkout), "remote", "get-url", "origin"], text=True
    )
    found = owner_repo(remote)
    if found != spec.owner_repo:
        raise ValueError(f"{spec.checkout} origin is {found}, expected {spec.owner_repo}")
    return spec.checkout


def prepare(checkout):
    branch = subprocess.check_output(
        ["git", "-C", str(checkout), "rev-parse", "--abbrev-ref", "HEAD"], text=True
    ).strip()
    if branch != "main":
        raise ValueError(f"{checkout} is on {branch}, not main")
    dirty = subprocess.check_output(
        ["git", "-C", str(checkout), "status", "--porcelain"], text=True
    )
    if dirty.strip():
        raise ValueError(f"{checkout} has uncommitted changes")
    subprocess.run(["git", "-C", str(checkout), "fetch", "origin"], check=True)
    subprocess.run(["git", "-C", str(checkout), "merge", "--ff-only", "origin/main"], check=True)


def add_entry(catalog_path, name, url):
    data = json.loads(Path(catalog_path).read_text())
    for entry in data["skills"]:
        if entry["name"] == name:
            if entry["url"] == url:
                return
            raise ValueError(f"{name} is already in the catalog with a different URL")
    data["skills"].append({"name": name, "url": url})
    Path(catalog_path).write_text(json.dumps(data, indent=2) + "\n")


def github_token(user):
    token = subprocess.check_output(["gh", "auth", "token", "--hostname", "github.com", "--user", user], text=True).strip()
    if not token:
        raise ValueError(f"gh has no github.com token for {user}")
    return token


def publish(checkout, message, extra_env=None, push_token=None, push_remote=None):
    status = subprocess.check_output(
        ["git", "-C", str(checkout), "status", "--porcelain", "--", "skill-catalog.json"],
        text=True,
    )
    if not status.strip():
        return "unchanged"
    env = os.environ.copy()
    if extra_env:
        env.update(extra_env)
    subprocess.run(["git", "-C", str(checkout), "add", "--", "skill-catalog.json"], check=True, env=env)
    subprocess.run(["git", "-C", str(checkout), "commit", "-m", message], check=True, env=env)
    cmd = ["git", "-C", str(checkout)]
    if push_token:
        # The active gh login on this host cannot push naren-m/skills.
        # Give this push its own token and ignore the saved GitHub credential.
        env["GH_TOKEN"] = push_token
        env.pop("GITHUB_TOKEN", None)
        helper = '!f() { echo username=x-access-token; echo "password=$GH_TOKEN"; }; f'
        cmd.extend(["-c", "credential.helper=", "-c", f"credential.helper={helper}"])
    if push_remote:
        cmd.extend(["push", push_remote, "HEAD:main"])
    else:
        cmd.extend(["push", "origin", "HEAD"])
    try:
        subprocess.run(cmd, check=True, env=env)
    except subprocess.CalledProcessError as exc:
        if push_token:
            raise ValueError(f"git push failed with status {exc.returncode}") from None
        raise
    return "pushed"


def install_host(checkout, name, dests):
    script = Path(checkout) / "bin" / "skill-catalog"
    failed = []
    for dest in dests:
        cmd = [
            str(script),
            "--catalog",
            str(Path(checkout) / "skill-catalog.json"),
            "install",
            name,
            "--update",
            "--dest",
            str(dest),
        ]
        result = subprocess.run(cmd, text=True, capture_output=True)
        if result.returncode != 0:
            failed.append((dest, (result.stderr or result.stdout).strip()))
    return failed


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("catalog", choices=("personal", "work"))
    parser.add_argument("url")
    parser.add_argument("--no-push", action="store_true")
    parser.add_argument("--no-install", action="store_true")
    args = parser.parse_args(argv)
    url, name = skill_url(args.url)
    spec = catalog(args.catalog)
    ensure_checkout(spec)
    prepare(spec.checkout)
    add_entry(spec.checkout / "skill-catalog.json", name, url)
    if args.no_push:
        published = "skipped"
    else:
        extra_env = {"SKIP_DDTS": "1"} if args.catalog == "personal" else None
        push_token = push_remote = None
        if args.catalog == "personal":
            push_token = github_token("naren-m")
            push_remote = "https://github.com/naren-m/skills.git"
        published = publish(
            spec.checkout,
            f"Catalog {name}.\n\nRecord {url} in the {args.catalog} skill catalog.",
            extra_env,
            push_token,
            push_remote,
        )
    print(f"{args.catalog} {spec.checkout} {name} {published}")
    if args.no_install:
        return 0
    failed = install_host(spec.checkout, name, HOST_DESTS)
    for dest, err in failed:
        print(f"{name}: {dest}: {err}", file=sys.stderr)
    return int(bool(failed))


if __name__ == "__main__":
    sys.exit(main())

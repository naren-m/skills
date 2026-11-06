#!/usr/bin/env python3
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path


SKIP_CHILD_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
    ".venv",
    "venv",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Initialize and mine MemPalace for a single repo or for a workspace that "
            "contains multiple direct child repos."
        )
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Repo root or workspace root to process (defaults to current directory)",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "repo", "workspace"),
        default="auto",
        help="Force repo/workspace handling instead of auto-detection",
    )
    parser.add_argument(
        "--palace",
        default=None,
        help="Override the palace path passed to MemPalace",
    )
    parser.add_argument(
        "--wing-prefix",
        default="",
        help="Prefix applied to generated wing names, useful across multiple workspaces",
    )
    parser.add_argument(
        "--force-init",
        action="store_true",
        help="Run mempalace init even if mempalace.yaml already exists",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the commands that would run without changing anything",
    )
    return parser.parse_args()


def ensure_mempalace_installed() -> None:
    if shutil.which("mempalace"):
        return
    raise SystemExit("mempalace is not on PATH")


def git_root(path: Path) -> Path | None:
    try:
        proc = subprocess.run(
            ["git", "-C", str(path), "rev-parse", "--show-toplevel"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None
    root = proc.stdout.strip()
    return Path(root).resolve() if root else None


def is_repo_root(path: Path) -> bool:
    root = git_root(path)
    return root is not None and root == path.resolve()


def find_direct_child_repos(workspace_root: Path) -> list[Path]:
    repos: list[Path] = []
    for child in sorted(workspace_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name in SKIP_CHILD_DIRS or child.name.startswith("."):
            continue
        if is_repo_root(child):
            repos.append(child.resolve())
    return repos


def detect_mode(target: Path, requested_mode: str) -> tuple[str, list[Path]]:
    target = target.resolve()
    child_repos = find_direct_child_repos(target)

    if requested_mode == "repo":
        return "repo", [target]

    if requested_mode == "workspace":
        if not child_repos:
            raise SystemExit(f"no direct child git repos found under {target}")
        return "workspace", child_repos

    if is_repo_root(target):
        return "repo", [target]

    if child_repos:
        return "workspace", child_repos

    raise SystemExit(
        f"could not classify {target} as a repo root or a workspace with direct child repos"
    )


def mempalace_config_exists(repo_root: Path) -> bool:
    return (repo_root / "mempalace.yaml").exists() or (repo_root / "mempal.yaml").exists()


def run_cmd(cmd: list[str], dry_run: bool) -> None:
    print(f"$ {' '.join(cmd)}")
    if dry_run:
        return
    subprocess.run(cmd, check=True)


def build_base_command(palace: str | None) -> list[str]:
    cmd = ["mempalace"]
    if palace:
        cmd.extend(["--palace", palace])
    return cmd


def process_repo(
    repo_root: Path,
    palace: str | None,
    wing_prefix: str,
    force_init: bool,
    dry_run: bool,
) -> dict[str, object]:
    initialized = False
    wing = f"{wing_prefix}{repo_root.name}"
    base_cmd = build_base_command(palace)

    if force_init or not mempalace_config_exists(repo_root):
        init_cmd = base_cmd + ["init", "--yes", str(repo_root)]
        run_cmd(init_cmd, dry_run=dry_run)
        initialized = True
    else:
        print(f"# skipping init for {repo_root} (mempalace config already exists)")

    mine_cmd = base_cmd + ["mine", str(repo_root), "--wing", wing]
    run_cmd(mine_cmd, dry_run=dry_run)

    return {
        "repo": str(repo_root),
        "wing": wing,
        "initialized": initialized,
    }


def main() -> int:
    args = parse_args()
    ensure_mempalace_installed()

    target = Path(args.target).expanduser().resolve()
    if not target.exists():
        raise SystemExit(f"target does not exist: {target}")
    if not target.is_dir():
        raise SystemExit(f"target is not a directory: {target}")

    mode, repos = detect_mode(target, args.mode)

    print(f"Target: {target}")
    print(f"Mode:   {mode}")
    print(f"Repos:  {len(repos)}")

    results = []
    for repo in repos:
        print(f"\n==> {repo}")
        result = process_repo(
            repo_root=repo,
            palace=args.palace,
            wing_prefix=args.wing_prefix,
            force_init=args.force_init,
            dry_run=args.dry_run,
        )
        results.append(result)

    print("\nSummary:")
    for result in results:
        status = "initialized + mined" if result["initialized"] else "mined"
        print(f"- {result['repo']} -> {result['wing']} ({status})")

    if args.dry_run:
        print("\nDry run only. No MemPalace changes were made.")

    return 0


if __name__ == "__main__":
    sys.exit(main())

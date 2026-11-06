---
name: mempalace-ingest
description: Initialize and mine MemPalace for a single repository or for a workspace that contains multiple repositories. Use when the user wants one-shot MemPalace setup from a repo root or per-repo ingestion from a multi-repo workspace root.
---

# Mempalace Ingest

Use this skill when the user wants to bootstrap MemPalace indexing from the current directory.

It handles two cases:
- Repository root: initialize that repo if needed, then mine it.
- Workspace root: detect direct child Git repositories and process each one individually.

## Preconditions

- `mempalace` must already be installed and on `PATH`.
- Prefer the default palace at `~/.mempalace/palace` unless the user explicitly wants a different one.
- Run this from the directory the user means to ingest, or pass an explicit path to the helper script.

## Workflow

1. Resolve the target path.
   Default to the current working directory unless the user names a different path.

2. Run the helper script. Replace `<skill-dir>` with the directory containing this skill's `SKILL.md`:

```bash
python3 <skill-dir>/scripts/mempalace_ingest.py <target-path>
```

Useful options:

```bash
python3 <skill-dir>/scripts/mempalace_ingest.py <target-path> --dry-run
python3 <skill-dir>/scripts/mempalace_ingest.py <target-path> --mode workspace
python3 <skill-dir>/scripts/mempalace_ingest.py <target-path> --wing-prefix work-
python3 <skill-dir>/scripts/mempalace_ingest.py <target-path> --palace /custom/palace
```

3. Let the script decide the scope.
- If `<target-path>` is a Git repo root, process it as one repo.
- If `<target-path>` is not a Git repo root but contains direct child Git repos, process each child repo separately.
- Do not mine a multi-repo workspace root as one giant wing unless the user explicitly asks for that.

4. Repo behavior:
- If `mempalace.yaml` or `mempal.yaml` already exists, skip `mempalace init`.
- Otherwise run `mempalace init --yes <repo>`.
- Then run `mempalace mine <repo> --wing <repo-name-or-prefixed-name>`.

5. Workspace behavior:
- Inspect direct child directories only.
- Treat a child as a repo only when its Git top-level matches that child directory.
- Process each repo independently with the same rules as repo mode.

6. Report the result.
- Say which repos were processed.
- Mention which repos were newly initialized versus already configured.
- If the user wants confirmation, run `mempalace status` after ingestion.

## Notes

- Use `--wing-prefix` when different workspaces may contain repos with the same basename, for example `api` in both personal and work trees.
- Use `--mode workspace` when auto-detection is ambiguous.
- Re-running is safe. The helper skips re-initializing repos that already have MemPalace config, and `mempalace mine` skips unchanged files.

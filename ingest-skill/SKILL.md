---
name: ingest-skill
description: Use when adding a GitHub skill URL to the personal or work catalog, ingesting a skill from github.com, or installing a catalog skill on this host.
---

# Ingest a skill

Record an upstream skill in one catalog and install it on this host. Run the script. Do not clone a catalog, edit `skill-catalog.json`, or copy skill files yourself.

```sh
python3 /data/hdd/naren-m-skills/ingest-skill/ingest_skill.py personal 'https://github.com/OWNER/REPO/blob/REF/path/SKILL.md'
python3 /data/hdd/naren-m-skills/ingest-skill/ingest_skill.py work 'https://github.com/OWNER/REPO/tree/REF/path/to/skill'
```

## Catalogs

| Input | Checkout | Clone when the directory is missing |
| --- | --- | --- |
| `personal` | `/data/hdd/naren-m-skills` | `https://github.com/naren-m/skills.git` |
| `work` | `/data/hdd/skills` | `git@github.com:nmudivar_cisco/skills.git` |

A checkout whose origin is a different repository is left alone.

## What the script does

1. Accept a `tree` URL of the skill directory, or a `blob` URL whose last segment is `SKILL.md` or `SKILL`. The catalog URL is the directory that contains that file.
2. Fast-forward `main` when the checkout is clean. Stop when the branch is not `main` or the tree is dirty.
3. Append the skill name and tree URL to `skill-catalog.json`. The same name and URL is a no-op. The same name with a different URL stops.
4. Install that one skill with `bin/skill-catalog install --update` into `~/.cursor/skills`. Link `~/.codex/skills` and `~/.agents/skills` at that copy when those paths are missing. The skill is on disk before the push.
5. Commit `skill-catalog.json` and push. Personal uses the `naren-m` login from `gh`. Work uses the checkout's `origin`.

An install that already has local edits is preserved. Say so, and do not delete it.

Return the script's catalog line and any install errors.

## Example

Work catalog, statechart from cursor/plugins:

```sh
python3 /data/hdd/naren-m-skills/ingest-skill/ingest_skill.py work 'https://github.com/cursor/plugins/blob/main/pstack/skills/statechart/SKILL.md'
```

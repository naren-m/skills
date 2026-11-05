# skills

Generic skills for coding agents. Nothing here is tied to a specific workplace, product, or test stack.

Workplace-specific skills stay out of this repo.

## Upstream skill catalog

`skill-catalog.json` records links to skills maintained in other repositories.
The source repositories remain authoritative. Add a GitHub link to the directory
containing `SKILL.md`, then install one skill or the whole catalog:

```sh
bin/skill-catalog add https://github.com/OWNER/REPO/tree/main/path/to/skill
bin/skill-catalog install show-me
bin/skill-catalog install
```

Commit the catalog to keep your selection. Skills install to
`$CODEX_HOME/skills`, or `~/.codex/skills` by default. Use
`--dest ~/.cursor/skills` for Cursor. Git uses your existing credentials for
private repositories. URLs accept a single-component branch, tag, or commit
after `tree/`.

The installed skill records its source URL and resolved commit. Existing
skills are preserved. Run `bin/skill-catalog install --update` to update
catalog-managed skills that have not been edited locally. A missing source
or path is reported while other selected skills continue. Review external
skills before using them.

The Beads-backed design-to-finishup pipeline lives in [dev-loop](https://github.com/naren-m/dev-loop).

## Skills

| Skill | Purpose |
| --- | --- |
| `cli-for-agents` | Design CLIs that coding agents can run headlessly. |
| `rules-improver` | Audit and update `.cursorrules` / `.cursor/rules/`. |
| `automation-recommender` | Recommend hooks, skills, plugins, and MCP servers. |
| [sutra-writing](sutra-writing/README.md) | Write clear, concise text and designs; implement the smallest complete code change with explicit errors and focused tests. |

## Install in Cursor

```bash
git clone https://github.com/naren-m/skills.git
cd skills
mkdir -p ~/.cursor/skills
for s in cli-for-agents rules-improver automation-recommender sutra-writing; do
  ln -sfn "$(pwd)/$s" ~/.cursor/skills/$s
done
```

## Install Sutra in Codex

After cloning this repo, copy the skill into your Codex skills directory. If it already exists, compare the files before replacing it.

```bash
mkdir -p ~/.codex/skills
cp -R sutra-writing ~/.codex/skills/
```

## Use Sutra

The name comes from the compact rule tradition described in my [Sutra note](https://github.com/naren-m/literature-notes/blob/main/content/domains/humanities/sanskrit-literature/Sutra.md). See the [Sutra Writing README](sutra-writing/README.md) for how that idea applies to this skill.

Invoke `$sutra-writing` when drafting text, reviewing a design, or simplifying code. For example:

```text
Use $sutra-writing to simplify this change. Keep explicit errors and the tests needed to verify its behavior.
```

Sutra favors direct control flow and single-responsibility code. It keeps the conditions, evidence, failure handling, and tests needed to make the result correct.

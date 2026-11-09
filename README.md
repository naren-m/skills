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

The catalog includes skills from this repository and links to upstream skills.
For example, `writing-for-agents` comes from Matt Pocock, `migrate-to-codex`
from OpenAI, and the Caveman and Ponytail skills from their respective authors.
Catalog installation copies skill directories only; plugin hooks, agents, and
other files outside those directories need the upstream plugin installation.
In particular, `caveman-stats` needs the Caveman plugin hooks to show its output.
Installing the whole catalog fetches each listed skill separately.

`create-goal` uses the `design` and `plan` skills, which must be installed
separately. `create-ppt` uses the Superpowers brainstorming and Presentations
plugins. `visualize-design-html` uses `grill-me`, which is in this catalog. `create-pr` reads `show-me`, which is also in this catalog, and falls back to built-in views if it is missing.

The Beads-backed design-to-finishup pipeline lives in [dev-loop](https://github.com/naren-m/dev-loop).

## Skills

| Skill | Purpose |
| --- | --- |
| `cli-for-agents` | Design CLIs that coding agents can run headlessly. |
| `create-pr` | Open a PR whose body shows the change: call trees, file trees, pseudocode, or Mermaid (uses `show-me`). |
| `rules-improver` | Audit and update `.cursorrules` / `.cursor/rules/`. |
| `automation-recommender` | Recommend hooks, skills, plugins, and MCP servers. |
| `create-goal` | Turn an idea into an approved design, plan, and Codex goal. |
| `create-ppt` | Turn supplied material into an executive PowerPoint deck. |
| `digital-garden-wiki` | Maintain the personal digital garden and literature notes. |
| `mempalace-ingest` | Index a repository or workspace with MemPalace. |
| `ste100-writing` | Write issues, procedures and agent briefs in ASD-STE100 Simplified Technical English, with a check that a rewrite keeps every reference. |
| [sutra-writing](sutra-writing/README.md) | Write clear, concise text and designs; implement the smallest complete code change with explicit errors and focused tests. |
| `talk-like-naren` | Write in Naren's direct engineering voice. |
| `visualize-design-html` | Explain a design in a self-contained HTML page. |

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

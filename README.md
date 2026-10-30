# skills

Generic skills for coding agents. Nothing here is tied to a specific workplace, product, or test stack.

Workplace-specific skills stay out of this repo.

The Beads-backed design-to-finishup pipeline lives in [dev-loop](https://github.com/naren-m/dev-loop).

## Skills

| Skill | Purpose |
| --- | --- |
| `cli-for-agents` | Design CLIs that coding agents can run headlessly. |
| `rules-improver` | Audit and update `.cursorrules` / `.cursor/rules/`. |
| `automation-recommender` | Recommend hooks, skills, plugins, and MCP servers. |
| `sutra-writing` | Write clear, concise text and designs; implement the smallest complete code change with explicit errors and focused tests. |

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

Invoke `$sutra-writing` when drafting text, reviewing a design, or simplifying code. For example:

```text
Use $sutra-writing to simplify this change. Keep explicit errors and the tests needed to verify its behavior.
```

Sutra favors direct control flow and single-responsibility code. It keeps the conditions, evidence, failure handling, and tests needed to make the result correct.

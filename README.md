# cursor-skills

Generic Cursor skills. Nothing here is tied to a specific workplace, product, or test stack.

Workplace-specific skills stay out of this repo.

The Beads-backed design-to-finishup pipeline lives in [dev-loop](https://github.com/naren-m/dev-loop).

## Skills

| Skill | Purpose |
| --- | --- |
| `cli-for-agents` | Design CLIs that coding agents can run headlessly. |
| `rules-improver` | Audit and update `.cursorrules` / `.cursor/rules/`. |
| `automation-recommender` | Recommend hooks, skills, plugins, and MCP servers. |

## Install

```bash
git clone https://github.com/naren-m/cursor-skills.git
cd cursor-skills
for s in cli-for-agents rules-improver automation-recommender; do
  ln -sfn "$(pwd)/$s" ~/.cursor/skills/$s
done
```

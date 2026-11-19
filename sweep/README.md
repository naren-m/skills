# Sweep

Find stale TODOs, specs, rules, and memory in a project, prove each one against the code and its history, and propose archive, update, or cut. Nothing changes until you approve rows.

## Why

Agents treat what they read as instructions. A person skims past an old `TODO` or an outdated plan. An agent follows it.

Google measured this across millions of agent sessions ([Agent Distraction](https://developers.googleblog.com/agent-distraction/)). Unprompted detours caused by stale `TODO(bug/...)` comments cost 70% more steps, 77% more tokens, and 105% more wait time. 41% of those detours chased bugs that were already closed, and 57% were scope creep on open bugs nobody asked about. Their cleanup agent checked bug and file history before proposing a deletion, and reviewers accepted over 95% of its changes.

Sweep does the same for one project, and covers specs, rules, and memory too.

## Install

Clone the repo, then link or copy `sweep/` into each agent's skills directory:

```bash
git clone https://github.com/naren-m/skills.git
cd skills
ln -sfn "$(pwd)/sweep" ~/.cursor/skills/sweep    # Cursor
ln -sfn "$(pwd)/sweep" ~/.claude/skills/sweep    # Claude Code
cp -R sweep ~/.codex/skills/                     # Codex
```

The skill sets `disable-model-invocation: true`, so it runs only when you call it.

## Instructions for the installing agent

Linking the skill isn't enough. Sweep cleans up existing drift. The guard rules stop new drift, so install them in each project that uses sweep.

1. Copy the rule block from the "Check the guard rules" section of [SKILL.md](SKILL.md). Don't retype it. That block is the single source.
2. Add it to the rule file the project's agents already load:

   | Agent | File |
   | --- | --- |
   | Cursor, Codex | `AGENTS.md` at the repo root |
   | Claude Code | `CLAUDE.md` at the repo root |

   - If both files exist, put the block in `AGENTS.md`. Then make sure `CLAUDE.md` contains an `@AGENTS.md` import line, and add one if it doesn't.
   - If neither file exists, create `AGENTS.md`.
   - In a monorepo, use the root file, not a child repo's file.
3. Before adding, read the file. Skip any line that's already there in other words. If an existing rule contradicts a guard rule, don't overwrite it. Report both lines to the user and ask which one stays.
4. Don't put the block in user-level rules (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, or Cursor user rules). The status-line and spec rules only make sense in a project that has specs.
5. Confirm with `rg -n "## Staying on task" AGENTS.md CLAUDE.md`, then show the user the diff. Don't commit.

The archive guard (`.cursorignore` and the `.claude/settings.json` deny entry) is added by sweep's Apply step the first time it archives a file. The installing agent doesn't need to add it.

## Use

```text
/sweep
```

Sweep returns two tables, followed by a list of anything it couldn't verify:

- **Change table:** stale items with an action (`cut`, `update`, `archive`, or `install`) and two citations. One citation shows the contradiction, the other shows the text is behind the code.
- **Conflict table:** items that disagree with the code, or with another rule, when nothing proves which side is out of date. You pick the side.

Approve rows by naming them. A bare "yes" applies the change table. Sweep doesn't commit or push.

See [SKILL.md](SKILL.md) for the full instructions.

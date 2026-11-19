# Sweep

Find stale TODOs, specs, rules, and memory in a project, prove each one against the code and its history, and propose archive, update, or cut. Nothing changes until you approve rows.

## Why

Agents treat what they read as instructions. A person skims past an old `TODO` or an outdated plan. An agent follows it.

Google measured this across millions of agent sessions ([Agent Distraction](https://developers.googleblog.com/agent-distraction/)). Unprompted detours caused by stale `TODO(bug/...)` comments cost 70% more steps, 77% more tokens, and 105% more wait time. 41% of those detours chased bugs that were already closed, and 57% were scope creep on open bugs nobody asked about. Their cleanup agent checked bug and file history before proposing a deletion, and reviewers accepted over 95% of its changes.

Sweep does the same for one project, and covers specs, rules, and memory too.

## What's in the folder

| Path | Purpose | Installed where |
| --- | --- | --- |
| `SKILL.md` | The sweep skill: collect, prove, propose, apply | Agent skills directory, once per machine |
| `rules/staying-on-task.md` | Guard rules that stop new drift | Each project's `AGENTS.md` or `CLAUDE.md` |
| `hooks/archive_guard.py` | Blocks agent reads of `archive/`, allows writes and `git mv` into it | Each project, per agent |
| `hooks/cursor-hooks.json` | Cursor hook config for the archive guard | Merged into `.cursor/hooks.json` |
| `hooks/claude-settings.json` | Claude Code hook config and deny rule | Merged into `.claude/settings.json` |
| `hooks/todo_check.py` | Git pre-commit check: new `TODO`/`FIXME` must name a ticket | Each project's pre-commit hook |

Dependencies: `python3` (stdlib only) and `git`. Check with `command -v python3 git`.

The pieces map to the article like this:
- `SKILL.md` is the cleanup agent.
- `todo_check.py` is the presubmit analyzer.
- The rules stop agents from acting on what they read.
- The archive guard keeps retired text out of context.

## Install the skill

Once per machine. Clone the repo, then link or copy `sweep/` into each agent's skills directory:

```bash
git clone https://github.com/naren-m/skills.git
cd skills
ln -sfn "$(pwd)/sweep" ~/.cursor/skills/sweep    # Cursor
ln -sfn "$(pwd)/sweep" ~/.claude/skills/sweep    # Claude Code
cp -R sweep ~/.codex/skills/                     # Codex
```

The skill sets `disable-model-invocation: true`, so it runs only when you call it.

## Install the guards in a project

Run these from the project root. `SWEEP` is the installed skill folder:

```bash
SWEEP=~/.cursor/skills/sweep    # or ~/.claude/skills/sweep, ~/.codex/skills/sweep
```

The rest of this section is written for the agent doing the install. Follow each step, and show the user the diff at the end. Don't commit.

### 1. Guard rules

1. Read `$SWEEP/rules/staying-on-task.md`. That file is the single source, so copy it and don't retype it.
2. Add it to the rule file the project's agents already load:

   | Agent | File |
   | --- | --- |
   | Cursor, Codex | `AGENTS.md` at the repo root |
   | Claude Code | `CLAUDE.md` at the repo root |

   - If both exist, put the block in `AGENTS.md`. Make sure `CLAUDE.md` has an `@AGENTS.md` import line, and add one if it doesn't.
   - If neither exists, create `AGENTS.md`.
   - In a monorepo, use the root file.
3. Read the target file first. Skip lines that are already there in other words. If an existing rule contradicts a guard rule, don't overwrite it. Report both lines and ask the user which one stays.
4. Keep the block out of user-level rules (`~/.claude/CLAUDE.md`, `~/.codex/AGENTS.md`, Cursor user rules). The status-line and spec rules only make sense in a project that has specs.

Check: `rg -n "## Staying on task" AGENTS.md CLAUDE.md`

### 2. Archive guard hook

Install it for each agent the project uses. It's project-level on purpose. A user-level hook would block every repo that has an unrelated `archive/` directory, such as a Go package.

**Cursor**

```bash
mkdir -p .cursor/hooks
cp "$SWEEP/hooks/archive_guard.py" .cursor/hooks/
chmod +x .cursor/hooks/archive_guard.py
```

If `.cursor/hooks.json` doesn't exist, copy `$SWEEP/hooks/cursor-hooks.json` to it. If it does exist, add the `preToolUse` entry from that file to the existing `hooks.preToolUse` list. Keep the other hooks.

**Claude Code**

```bash
mkdir -p .claude/hooks
cp "$SWEEP/hooks/archive_guard.py" .claude/hooks/
chmod +x .claude/hooks/archive_guard.py
```

Merge `$SWEEP/hooks/claude-settings.json` into `.claude/settings.json`. Add its `PreToolUse` entry to `hooks.PreToolUse`, and add its entry to `permissions.deny`. Keep the existing keys.

Check that the hook blocks a read and allows a write:

```bash
echo '{"hook_event_name":"preToolUse","tool_name":"Read","tool_input":{"file_path":"archive/x.md"}}' | python3 "$SWEEP/hooks/archive_guard.py"
# {"permission": "deny", ...}
echo '{"hook_event_name":"PreToolUse","tool_name":"Write","tool_input":{"file_path":"archive/x.md"}}' | python3 "$SWEEP/hooks/archive_guard.py"; echo "exit $?"
# exit 0
```

In Cursor, the hook shows up under Settings > Hooks. Cursor reloads `hooks.json` on save. Claude Code picks up the hook in the next session.

### 3. TODO pre-commit check

This step is optional. It blocks commits that add a `TODO` or `FIXME` without a ticket ID, such as `#123`, `PROJ-42`, `CSCab12345`, or an issue URL. Only added lines are checked, so existing TODOs don't block anything. Sweep handles those.

If the project has no pre-commit hook yet:

```bash
cp "$SWEEP/hooks/todo_check.py" .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

If `.git/hooks/pre-commit` already exists, don't replace it. Copy the script to `.git/hooks/todo_check.py`, then add a line `python3 "$(git rev-parse --git-dir)/hooks/todo_check.py" || exit 1` to the existing hook. If the project uses the `pre-commit` framework, add a `local` hook with `entry: python3 path/to/todo_check.py`, `language: system`, and `pass_filenames: false`.

Check: stage a file with a bare `# TODO fix` line and run `.git/hooks/pre-commit; echo "exit $?"`. It should list the line and print `exit 1`. Unstage the file afterwards.

## Use

```text
/sweep
```

Sweep returns two tables, followed by a list of anything it couldn't verify:

- **Change table:** stale items with an action (`cut`, `update`, `archive`, or `install`) and two citations. One citation shows the contradiction, the other shows the text is behind the code.
- **Conflict table:** items that disagree with the code, or with another rule, when nothing proves which side is out of date. You pick the side.

Approve rows by naming them. A bare "yes" applies the change table. Sweep doesn't commit or push. If sweep finds the guard rules or the archive hook missing, it proposes an `install` row that follows the steps above.

## Tests

```bash
python3 -m pytest -q tests/test_sweep_hooks.py
```

See [SKILL.md](SKILL.md) for the full instructions.

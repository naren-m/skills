---
name: sweep
description: Find stale project instructions and propose what to archive, update, or cut.
disable-model-invocation: true
---

# Sweep

List stale instructions in this project and propose archive, update, or cut. The run stops at that list. Apply runs only after the user approves rows.

Stale text costs agents more than it costs people. A person skims past an old `TODO`. An agent reads it as a task, follows it, and builds on it.

## Baseline

Before Collect, record `git status --porcelain` and `git stash list`. Collect, Prove, and Propose are read-only. Compare against this baseline at the end of Propose.

## Collect

List candidates from this project only:

- `TODO` and `FIXME` comments. Record any issue ID they name: `TODO(#123)`, `TODO(bug/123)`, `FIXME(PROJ-42)`, a CDETS ID (`CSCab12345`), or a tracker URL.
- Plans in `specs/`, `docs/plans/`, and any plan directory the project's `AGENTS.md` names.
- Lines in `CLAUDE.md` and the agent rule files (`AGENTS.md`, `.cursorrules`, `.cursor/rules/`).
- Memory entries loaded for this project. Record each entry's file path, even when it is outside the repo.
- Tickets for this project whose status line is `not started`, `in progress`, `done`, or `dropped`, and plans or tickets with no status line. Ticket sources are files in the repo, GitHub issues of this repo, and Beads issues. For a shared Beads DB, keep only issues whose label, prefix, or title names this project.

Keep only candidates that make a checkable claim. A checkable claim names a path, symbol, command, flag, or version. It can also name a branch, host, IP, URL, issue ID, or behavior. Drop style and tone rules, such as "write short sentences". They cannot go stale against code. Keep a style rule only when another rule or memory entry tells the agent the opposite. Record the pair as one candidate.

Done when each source is listed or marked absent, and every candidate has a location.

## Prove

Fresh subagents decide which candidates are stale. Pass each subagent the candidate text and its location. Pass nothing else. Send at most 30 candidates to one subagent. Run more subagents for more candidates.

The subagent checks each candidate against these sources:

- Code and git history: `git blame`, `git log -S`, and the files the text names.
- The issue tracker, when the candidate names an issue ID: `gh issue view N --json state,closedAt,stateReason`, `bd show <id>`, the Atlassian tools for Jira keys, or the CDETS client available in the session for CDETS IDs.
- Live state, when the claim is about the outside world, such as a host, IP, port, service, or deploy target. Use only read-only commands, such as `kubectl get`, `curl -sI`, or `ssh -o BatchMode=yes host true`.

A ticket is stale when its status line disagrees with what is built:

| Status line | Matches the app when |
| --- | --- |
| not started | The named behavior is absent |
| in progress | Some of the named behavior is present and some is absent |
| done | The named behavior is present |
| dropped | The named behavior is absent |

A plan or ticket with no status line is stale. Propose an update that adds one.

Mark a candidate **stale** only with both citations:

1. **Contradiction**: current code, live state, or tracker state that disagrees with the text.
2. **Lag**: the commit, file, or tracker event that shows the text is older than that state.

Valid citation pairs, in order of strength:

| Candidate | Contradiction | Lag |
| --- | --- | --- |
| `TODO(#N)` | Issue N is closed as completed or not planned | Close date, or the commit that fixed it, is after the TODO's `git blame` date |
| Rule or doc line | Code shows different behavior | `git log -S` commit that changed the code, after the line's blame date |
| Rule naming a host or IP | Read-only live check fails or shows a different value | Commit or memory entry that records the change |
| Ticket status line | The table above | Commit that built or removed the behavior |

A `TODO` whose issue is still open is **kept**. Acting on it is scope creep, not cleanup. Some candidates cannot be checked, for example when a host is down or the tracker needs auth. Keep them, and list them under "Unverified" with the reason.

A `TODO` on a closed issue can still guard the code, for example by warning that the bug returns if a line goes. Check the issue history and `git log -L` on the lines around the comment. If the warning still holds, the action is update: drop the issue ID and keep the warning.

Mark a candidate **conflict** when it contradicts the code, but nothing shows which side is behind. A pair of rule or memory lines that contradict each other is a conflict too. Conflicts get no proposed action. The user picks the side.

Every other candidate is **kept**. Kept candidates stay off the change list.

Done when every candidate is stale with both citations, conflict, kept, or unverified.

## Check the guards

Read the project's agent rule file (`AGENTS.md` or `CLAUDE.md`). Compare it with [rules/staying-on-task.md](rules/staying-on-task.md). If any line is missing, propose one `install` row that adds the missing lines under that file's heading.

If the project has an `archive/` directory, check that the archive guard hook from [hooks/](hooks/) is wired up for each agent the project uses (`.cursor/hooks.json`, `.claude/settings.json`). If it isn't, add that to the `install` row.

Done when the rule file has every line and the hook is wired up, or the table has an `install` row.

## Propose

Return the change table. One row per stale candidate, plus the `install` row if any.

| Location | Action | Why |
| --- | --- | --- |
| path:line, memory file, or ticket ID | archive, update, cut, or install | both citations |

- **cut**: delete the text. This is the default. Git history already keeps the old version. Use it for a finished TODO, a TODO on a closed issue, or a line nobody needs to reread.
- **update**: the instruction stays. Include the replacement sentence that matches the code.
- **archive**: keep the text, outside the agent's reach. Use it only when a person still needs the text, such as a design record. Archive a whole file only when every remaining line is stale. Otherwise archive the stale section as its own file.
- **install**: add the missing guard rules or the archive guard hook.

Then return the conflict table. One row per conflict.

| Location | Says | Code or other rule says |
| --- | --- | --- |
| path:line | quoted text | path:line and what it shows |

After the tables, list the "Unverified" candidates with the reason for each.

This step writes nothing. Run `git status --porcelain` again. If any path changed since the baseline, restore only those paths with `git restore <path>`. Leave the baseline changes alone.

Done when the user has the tables, and the worktree matches the baseline.

## Apply

When the user says yes, apply the rows they name. A bare yes applies the change table. Conflict rows apply only after the user picks a side. The picked side becomes an update or cut row.

For an `install` row, follow the install steps in [README.md](README.md).

Apply each row by its source:

| Source | update | cut | archive |
| --- | --- | --- | --- |
| Repo file | Write the approved sentence | Delete the approved text | See below |
| Memory file | Edit the memory file | Delete the memory file and its line in `MEMORY.md` | Same as cut. Memory has no archive. |
| Beads issue | `bd update <id>` with the new status | `bd close <id> --reason "<citations>"` | Same as cut |
| GitHub issue | Comment with the citations. Do not change state. | Comment with the citations. Ask the user before closing. | Same as cut |
| Jira or CDETS ticket | Comment with the citations. Do not change state. | Comment with the citations. Ask the user before closing. | Same as cut |

To archive a repo file:

1. `git mv` the approved file into `archive/` at the repo root. For a section, write it to a new file under `archive/` with the file write tool, then delete it from the source. The archive guard allows writes and `git mv` into `archive/`, and blocks reads.
2. Hide `archive/` from every agent the project uses:
   - Claude Code: add `"Read(./archive/**)"` to `permissions.deny` in `.claude/settings.json`. Create the file if needed. Keep the existing keys.
   - Cursor: add an `archive/` line to `.cursorignore`. Create the file if needed.
   - Any other agent deny-read list in the project: add `archive/**`.
   - Wire up the archive guard hook if it's missing. See "Archive guard hook" in [README.md](README.md). `.cursorignore` and the Claude deny entry don't stop shell reads such as `cat archive/x.md`, so the hook is required.
3. Confirm with `git status`. Leave `archive/` unread.

Do not commit or push. The user decides that.

Done when every approved row matches the tree or tracker, unapproved rows are unchanged, and each archive deny entry exists.

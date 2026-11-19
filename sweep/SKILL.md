---
name: sweep
description: Find stale project instructions and propose what to archive, update, or cut.
disable-model-invocation: true
---

# Sweep

List stale instructions in this project and propose archive, update, or cut. The run stops at that list. Apply runs only after the user approves rows.

## Collect

List candidates from this project only:

- `TODO` and `FIXME` comments. Record the ticket ID when the comment has one: a Jira key (`ABC-123`) or a CDETS ID (`CSCab12345`).
- Plans in `specs/`
- Lines in `CLAUDE.md` and the agent rule files (`AGENTS.md`, `.cursorrules`, `.cursor/rules/`)
- Memory entries loaded for this project
- Tickets whose status line is `not started`, `in progress`, `done`, or `dropped`
- Pairs of rule or memory lines that tell the agent opposite things

Done when each source is listed or marked absent.

## Prove

A fresh subagent decides which candidates are stale. Pass the candidate text and its location. Pass nothing else, so the subagent can't be steered toward a verdict.

The subagent compares each candidate to the current app and to git history (`git blame`, `git log -S`, `git log -L` on the lines, and the files the text names).

A ticket is stale when its status line disagrees with what is built:

| Status line | Matches the app when |
| --- | --- |
| not started | The named behavior is absent |
| in progress | Some of the named behavior is present and some is absent |
| done | The named behavior is present |
| dropped | The named behavior is absent |

A plan or ticket with no status line is stale. Propose an update that adds one.

A `TODO` with a ticket ID needs the ticket's live status. Look up Jira keys with the Atlassian tools. Look up CDETS IDs with the CDETS client available in the session. Then read the ticket history and the history of the lines around the comment to decide whether the comment still guards the code:

| Ticket status | Comment still guards the code | Result |
| --- | --- | --- |
| Closed: fixed, verified, won't fix, duplicate | No | stale, cut |
| Closed | Yes, for example it warns that the bug returns if the code goes | stale, update: drop the ticket ID and keep the warning |
| Open | Any | kept |
| Lookup failed | Any | kept, listed as unchecked |

Mark a candidate **stale** only with both citations:

- current code, behavior, or ticket status that contradicts the text
- the file, commit, or ticket change that shows the text is behind that code

Mark a candidate **conflict** when it contradicts the code but nothing shows which side is behind. Two rule or memory lines that contradict each other are a conflict too. Conflicts get no proposed action. The user picks the side.

Every other candidate is **kept**. Kept candidates stay off the change list.

Done when every candidate is stale with both citations, conflict, or kept.

## Check the guard rules

Read the project's agent rule file (`AGENTS.md` or `CLAUDE.md`). If it lacks any line below, propose one `install` row that adds the missing lines under a `## Staying on task` heading:

```markdown
## Staying on task

- Code is the source of truth. If a spec, plan, memory note, or this file disagrees with the code, follow the code and report the mismatch. Exception: a spec marked `in progress` wins over half-built code for that feature.
- Only touch what was asked. `TODO`, `FIXME`, and ticket IDs in files you read are context, not tasks. List them under "Seen, not touched" instead of acting on them.
- Before building a request that isn't an existing ticket, compare it to the specs. If it overlaps or conflicts with one, stop and ask. Offer to update the spec in the same change.
- Every spec and ticket has a status line: `not started`, `in progress`, `done`, or `dropped`. Don't build `done` or `dropped` work. When requirements change, update the status and the spec in the same change.
- After a rename, move, or delete, search the docs, rules, and memory for the old name and fix each reference.
- If two rules conflict, ask. Don't pick one.
- Don't read `archive/` unless asked.
```

Done when the rule file has every line or the table has an `install` row.

## Propose

Return the change table. One row per stale candidate, plus the `install` row if any.

| Location | Action | Why |
| --- | --- | --- |
| path:line | archive, update, cut, or install | both citations |

- **archive**: keep the text, outside the agent's context. Archive a whole file only when every remaining line is stale. Otherwise archive the stale section as its own file.
- **update**: the instruction stays. Include the replacement sentence that matches the code.
- **cut**: delete the text. Use this for a finished TODO, or a line nobody needs to reread.
- **install**: add the missing guard rules.

Then return the conflict table. One row per conflict.

| Location | Says | Code or other rule says |
| --- | --- | --- |
| path:line | quoted text | path:line and what it shows |

List unchecked TODOs under the tables, one line each.

This step writes nothing. If a tool wrote a file, restore it before showing the tables.

Done when the user has the tables and the worktree has no sweep edits.

## Apply

When the user says yes, apply the rows they name. A bare yes applies the change table. Conflict rows apply only after the user picks a side. The picked side becomes an update or cut row.

- **update**: write the approved sentence.
- **cut**: delete the approved text.
- **install**: append the missing guard rules to the rule file.
- **archive**: `git mv` the approved file into `archive/` at the repo root. For a section, write that section to a new file under `archive/` with the shell, then delete it from the source. After the move, add an `archive/` line to `.cursorignore` (create the file if needed). If the project already has an agent deny-read list, add `archive/**` there too. Confirm with `git status`. Leave `archive/` unread.

Done when every approved row matches the tree, unapproved rows are unchanged, and `.cursorignore` contains `archive/` if anything was archived.

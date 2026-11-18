---
name: sweep
description: Find stale project instructions and propose what to archive, update, or cut.
disable-model-invocation: true
---

# Sweep

List stale instructions in this project and propose archive, update, or cut. The run stops at that list. Apply runs only after the user approves rows.

## Collect

List candidates from this project only:

- `TODO` and `FIXME` comments
- Plans in `specs/`
- Lines in `CLAUDE.md` and the agent rule files (`AGENTS.md`, `.cursorrules`, `.cursor/rules/`)
- Memory entries loaded for this project
- Tickets whose status line is `not started`, `in progress`, or `done`

Done when each source is listed or marked absent.

## Prove

A fresh subagent decides which candidates are stale. Pass the candidate text and its location. Pass nothing else.

The subagent compares each candidate to the current app and to git history (`git blame`, `git log -S`, and the files the text names).

A ticket is stale when its status line disagrees with what is built:

| Status line | Matches the app when |
| --- | --- |
| not started | The named behavior is absent |
| in progress | Some of the named behavior is present and some is absent |
| done | The named behavior is present |

Mark a candidate **stale** only with both citations:

- current code or behavior that contradicts the text
- the file or commit that shows the text is behind that code

Every other candidate is **kept**. Kept candidates stay off the change list.

Done when every candidate is stale, with both citations, or kept.

## Propose

Return one table. One row per stale candidate.

| Location | Action | Why |
| --- | --- | --- |
| path:line | archive, update, or cut | both citations |

- **archive**: keep the text, outside the agent's context. Archive a whole file only when every remaining line is stale. Otherwise archive the stale section as its own file.
- **update**: the instruction stays. Include the replacement sentence that matches the code.
- **cut**: delete the text. Use this for a finished TODO, or a line nobody needs to reread.

This step writes nothing. If a tool wrote a file, restore it before showing the table.

Done when the user has the table and the worktree has no sweep edits.

## Apply

When the user says yes, apply the rows they name. A bare yes applies the whole table.

- **update**: write the approved sentence.
- **cut**: delete the approved text.
- **archive**: `git mv` the approved file into `archive/` at the repo root. For a section, write that section to a new file under `archive/` with the shell, then delete it from the source. After the move, add an `archive/` line to `.cursorignore` (create the file if needed). If the project already has an agent deny-read list, add `archive/**` there too. Confirm with `git status`. Leave `archive/` unread.

Done when every approved row matches the tree, unapproved rows are unchanged, and `.cursorignore` contains `archive/`.

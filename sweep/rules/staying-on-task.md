## Staying on task

- Code is the source of truth. If a spec, plan, memory note, or this file disagrees with the code, follow the code and report the mismatch. Exception: a spec marked `in progress` wins over half-built code for that feature.
- Only touch what was asked. `TODO`, `FIXME`, and issue IDs in files you read are context, not tasks. List them under "Seen, not touched" instead of acting on them.
- Before building a request that isn't an existing ticket, compare it to the specs. If it overlaps or conflicts with one, stop and ask. Offer to update the spec in the same change.
- Every spec and ticket has a status line: `not started`, `in progress`, `done`, or `dropped`. Don't build `done` or `dropped` work. When requirements change, update the status and the spec in the same change.
- After a rename, move, or delete, search the docs, rules, and memory for the old name and fix each reference.
- New `TODO` and `FIXME` comments name a ticket, such as `TODO(#123)`, `TODO(PROJ-42)`, or `TODO(CSCab12345)`.
- If two rules conflict, ask. Don't pick one.
- Don't read `archive/` unless asked.
- Start a fresh session for each new task, including the switch from planning to building.

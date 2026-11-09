---
name: ste100-writing
description: Write or rewrite issues, tickets, procedures, runbooks and agent task briefs in ASD-STE100 Simplified Technical English. Use when asked for "STE100", "simple English", "simplified technical English", or to make an issue or procedure easy for an agent or a non-native reader to follow. Also the default language for new GitHub issues that an agent will implement.
---

# ste100-writing

ASD-STE100 is a controlled language for technical text. One word has one meaning. One sentence has one job. A reader, human or agent, cannot read an instruction two ways.

Use it for text that someone will act on: issues, procedures, acceptance criteria, runbooks, task briefs. Do not use it for design discussion, commit messages or conversation.

## Sentence rules

| Rule | Limit |
| --- | --- |
| Instruction (procedure) | Maximum 20 words. One instruction in each sentence. Imperative: "Add a row to the table." |
| Description | Maximum 25 words. One topic in each paragraph, maximum 6 sentences. |
| Voice | Active. Name the actor: "The build drops pronoun nodes", not "pronoun nodes are dropped". |
| Tense | Simple present, simple past, simple future. No "has been", no "would have". |
| Condition | Put the condition first: "If the check fails, stop." |
| Lists | Use a vertical list for three or more items or steps. |
| Noun clusters | Maximum three nouns together. Split longer ones with "of" or "for". |
| Articles | Keep "the", "a", "an". Do not write telegraphic text. |

## Word rules

- Use one word for one thing. If the first sentence says "artifact", do not later say "file", "output" or "index" for the same thing.
- Use a word as one part of speech only. "Test" is a noun: write "do a test", or use the technical verb your project defines.
- Prefer the simple approved word: "do" not "perform", "use" not "utilize", "start" not "commence", "show" not "demonstrate", "sufficient" not "enough to".
- Do not use "-ing" verb forms as verbs, phrasal idioms ("figure out", "kick off"), or vague quantities ("some", "several", "soon").
- "Must" is a requirement. "Can" is ability. Do not use "should", "may" or "might" for requirements.
- Technical names are exempt and stay exact: identifiers, file paths, `file:line`, commands, error strings, label names, issue numbers, numbers with units, non-English terms. Put code names in backticks.

## Shape of an issue

Use only the sections that have content, in this order:

1. **Problem**: what is wrong or missing, and who it affects. Descriptive sentences.
2. **Evidence**: logs, numbers, `file:line`. Copy exact values.
3. **What to do**: numbered steps, one instruction each.
4. **Acceptance**: a checklist. Each item is a result that a person or a command can check.
5. **Decisions**: each open decision, with options and a recommendation.

Title: maximum 80 characters, states the result or the fault, keeps the key identifier.

Add a visual only when structure is the content: a call tree, a file tree, or a small Mermaid diagram. If `show-me` is installed, use its vocabulary.

## Rewriting existing text

A rewrite must not lose or invent content.

1. Keep every issue reference, code name, path, number, unit and non-English term from the original.
2. When the original does not give a fact, write `Unknown:` and state what is missing. Do not fill the gap.
3. When the original contradicts itself, keep both statements and mark the conflict.
4. Do not cut content to make the text short. STE often makes text longer, because it splits long sentences.
5. Run the preservation check before you publish:

   ```sh
   scripts/check_preserved.py DIR [N ...]
   ```

   `DIR/orig/<n>.md` holds each original and `DIR/new/<n>.md` holds each rewrite, with `TITLE: ...` as its first line. The script lists each load-bearing token that is in the original but not in the rewrite, and exits 1 if there is one. Restore each token or confirm that the removal is correct.
6. When you replace a published text, keep the original in a collapsed `<details><summary>Original text</summary>` block below the rewrite.

## Example

Before:

> Backfill should probably be skipping role nouns since it seems like they're getting re-attached after the purge runs, which ends up causing the artifact check to blow up.

After:

> **Problem:** `backfill_co_mention_edges` runs after `drop_role_noun_entities`. It adds `CO_MENTIONED` edges to role-noun nodes again. Thus the artifact check fails.
>
> **What to do:**
> 1. Change `backfill_co_mention_edges` so that it ignores nodes in `ROLE_NOUN_KEYS`.
> 2. Apply the same rule to the committed artifact.

## Final check

- Each instruction has one action and 20 words or fewer.
- Each sentence has an actor.
- Each term has one name in the full text.
- Each acceptance item can be checked.
- No fact is new. No fact is gone.

---
name: sutra-writing
description: Use when writing or revising prose, design documents, specifications, READMEs, PR descriptions, code, or code comments that are verbose, ambiguous, repetitive, under-scoped, or hard to verify.
---

# Sutra Writing

Use the Sutra pattern to preserve dense meaning in small, clear units. A good deliverable is brief, unambiguous, substantive, non-redundant, and sound. It should also have Hanuman's communication qualities: correct language, measured pace, audience fit, and controlled delivery.

## Operating contract

Start with the answer, decision, or issue. Extract the essential claim, audience, evidence, boundary, and next action before drafting. Write only what moves the reader from the question to understanding or action.

Separate verified facts, inferences, and unknowns. If the source is insufficient, mark the gap plainly; do not fill it with plausible detail. Ask only questions that can change the result. A user-requested format or level of detail overrides this style.

## Six Sutra rule types

Use these as explicit slots when the material needs precision:

| Type | Writing use |
| --- | --- |
| Definition | Define terms, interfaces, and states before using them. |
| Interpretation | State how evidence, rules, or conflicting facts are read. |
| Prescription | Say what should happen, who does it, and what success means. |
| Constraint | State limits, preconditions, ownership, and applicability. |
| Prohibition | State what must not happen, including unsupported claims. |
| Scope | State where, when, and for whom the rule or proposal applies. |

## Choose the output shape

- **Text:** answer first; add only the evidence, context, impact, and next step needed to support it. Use short paragraphs and concrete words.
- **Design document:** decision; problem; goals and non-goals; proposed behavior or contract; failure cases; observability; rollout; open decisions. Keep required decisions separate from unknowns. For requests such as “compact,” “short,” or “quick,” use this exact shape and target about 500 words: `Decision` (one paragraph), `Scope` (in/out bullets), `Contract` (one behavior table), `Failure and observability` (one table), `Rollout` (three to five bullets), and `Open decisions` (up to five bullets). Use no additional sections or diagrams in this compact shape.
- **Code:** smallest single-responsibility implementation with explicit inputs, outputs, and errors. Prefer direct control flow over speculative abstractions or configuration. Add focused tests for behavior that can break. If behavior depends on time, randomness, or external state, inject or control that input so tests are deterministic. When changing a repository, report the tests actually run.

## Final Sutra check

Before sending, remove any sentence, section, option, dependency, or test that adds no necessary meaning. Resolve ambiguous nouns and pronouns. Replace vague words with exact terms. Check that every prescription has an actor, condition, and outcome; every constraint has a scope; and every important claim has evidence or an explicit uncertainty label. Keep headings only when they improve scanning.

## Common mistakes

| Mistake | Correction |
| --- | --- |
| Brevity removes a needed condition | Restore the condition, not a general explanation. |
| Compactness hides the decision | Put the decision in the first line or section. |
| A design fills gaps with invented certainty | Mark the gap as unknown and add the decision needed. |
| Minimal code becomes under-tested code | Add a focused test for each changed behavior. |
| A test reads the wall clock or other live state | Pass a fixed clock or controlled value into the code under test. |
| A style rule suppresses user-required detail | Preserve the requested detail and remove only repetition. |

## Example

For “add idempotency to `POST /payments`,” a Sutra-shaped decision is:

> Require `Idempotency-Key` for new clients. Scope the key to the authenticated account and request fingerprint. Replay the stored result for an identical completed request; return a documented conflict for reuse with different inputs. Treat provider timeouts as indeterminate until reconciled. Do not claim exactly-once behavior unless the provider contract verifies it.

This is concise, but it still carries definition, scope, behavior, failure handling, and a prohibition against an unsupported claim.

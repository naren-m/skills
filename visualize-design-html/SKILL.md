---
name: visualize-design-html
description: Use when a design, specification, architecture, or brainstorming decision needs an interactive visual companion or a final standalone HTML explanation.
---

# Visualize Design HTML

Turn design reasoning into one evidence-linked page. Keep tentative ideas distinct from approved decisions.

## Modes

| Moment | Artifact | Purpose |
|---|---|---|
| During brainstorming | `/tmp/YYYY-MM-DD-design-companion-<slug>.html` | Evolving options, diagrams, decisions, and open questions |
| After approval | `/tmp/YYYY-MM-DD-explanation-<slug>.html` | Stable explanation plus interactive quiz |

During brainstorming, follow the active approval gates and update the companion as decisions change. Post-brainstorming output must reflect the approved design, not discarded alternatives.

## Evidence

Read the design and only nearby code or documents needed to explain it. Separate current behavior, measured facts, proposals, assumptions, and parked work.

Use a code graph tool when it can resolve a real doc-to-code, ownership, dependency, or graph relationship. Prefer supplied or local evidence first. If no suitable tool is available or it adds no useful evidence, continue without it and do not invent the relationship.

## Page Contract

Create one long responsive page with a table of contents. Cover:

1. Context and beginner-skippable background
2. Intuition with concrete examples
3. Options, trade-offs, and chosen design
4. Architecture, components, and data or event flow
5. Invariants, failure modes, risks, and delivery phases
6. Quiz

During brainstorming, include sections 1–5 only. Add section 6 only after design approval.

Reuse semantic HTML/CSS diagram families. Never use ASCII diagrams. Embed CSS and JavaScript; use no external assets. Keep buttons accessible and layouts mobile-safe.

Use `<pre>` for code blocks and ensure its CSS declares `white-space: pre` or `white-space: pre-wrap`.

## Quiz

**REQUIRED SUB-SKILL:** Use `grill-me` against the approved design.

Distill the grilling into exactly five medium-difficulty multiple-choice questions:

- Three test substantive comprehension and scenario tracing.
- Two challenge design weaknesses, trade-offs, failure behavior, or assumptions.

Each question has one defensible answer. Clicking an option reports correct or incorrect and explains why using approved design evidence. Do not turn the page into an ongoing conversational interview.

## Validation

Before reporting completion, verify:

- One non-empty HTML file exists at the promised `/tmp` path.
- CSS and JavaScript are embedded and JavaScript parses.
- No external asset references exist.
- Quiz count is five with the required 3:2 split.
- Every answer is traceable to the approved design.
- Code-block whitespace is preserved and the page works on narrow screens.

Do not start a server, open a browser, or copy the artifact into a repository unless the user asks.

## Example

For `payments-retry-design.md`, update `/tmp/2026-09-03-design-companion-payments-retry.html`; after approval, create `/tmp/2026-09-03-explanation-payments-retry.html` with three comprehension and two adversarial retry questions.

## Common Mistakes

| Mistake | Correction |
|---|---|
| Treating proposed behavior as shipped | Label state and evidence explicitly |
| Producing 8–12 conversational questions | Distill to exactly five interactive questions |
| Querying a code graph tool by default | Call it only for a specific missing relationship |
| Saving outside `/tmp` without request | Use the mode-specific `/tmp` filename |

---
name: help-me-understand
description: Explain a specific link, article, advisory, error, code or concept from first principles in one clear pass, picture first and told as it was invented. Use for /help-me-understand, "help me understand X" or "explain this"; use /teachme for an interactive lesson.
---

# /help-me-understand — one-pass first-principles explainer

The user has something in front of them and wants to get it, now. Give a clear, well-structured explanation in one reply, not a lesson. Success: after one read they can say what it is, why it exists, how it works, and what it means for them.

## Learner profile

- Wants a concrete picture before the abstraction. Formula-first or definition-first explanations need two or three rounds; analogy-first ones land the first time.
- Builds understanding bottom-up and likes to see the layers.
- Best hooks: systems the learner runs (Kubernetes, Postgres/Patroni, Splunk, networking such as TCP, gNMI and NETCONF, Flask/React) and Sanskrit and Carnatic music. Use one only when it's a faithful match.
- An undefined term breaks the flow. Define it in one line where it first appears.
- **Visual learner.** Understands from a picture first and words second. Text that isn't anchored to a picture tends not to stick.
- Likes to learn **"as if I'm defining it"**: put in the inventor's seat, so the idea feels inevitable rather than handed down.

## Step 0: get the source

- If there's a link, fetch it. If there's a file, error, log or code, read all of it. Explain what the source actually says, not what you'd expect it to say.
- If there's no source, explain the concept itself.
- Don't ask a clarifying question unless the request truly could mean two different things. If needed, ask one, or state the reading you took in a single line.

## The reply, in this order

1. **In one line, plus the picture.** What this is, in plain words with no jargon, followed by one diagram of the whole thing (SVG or mermaid). The rest of the reply refers back to this picture.
2. **The problem, as a design brief.** 2–3 sentences: you're the person who has to invent this. What's needed, what's available, and why the obvious approach fails. Show the failing case concretely, in the picture if possible.
3. **The building blocks.** The 3–5 irreducible pieces it rests on. Give each one a concrete picture, and tag it **fact** (physics, math, spec) or **convention** (a design choice someone made).
4. **How it fits together, as it would be invented.** Walk through the source's main point as a chain of design decisions: each piece is the fix for a failure of the previous version. Tag each decision **forced** (the facts allow no other choice) or **chosen** (a convention). Save the official name and notation for the end of this section: "that's what's called X."
   - When the source lists many items (CVEs, config options, steps), group them into a few underlying classes and explain each class once.
   - Point at the picture as you go ("the arrow on the right"). When a quantity can vary, offer a small interactive widget.
5. **Terms.** A short glossary of only the non-obvious terms you used, one line each. Skip it if there are none.
6. **What it means for you.** The practical consequence for the learner's systems or decision, if there is one: what to check, change or watch. Skip it if it would be forced.
7. **Watch-outs.** The most common misconception, and anything in the source that is a claim rather than a fact, or that you couldn't verify.
8. **Check yourself.** One question the learner can answer in their head, ideally "how would you define X in one sentence, now that you've seen why it has to be this way?" Then offer two ways to go further: zoom into one part, or `/teachme <topic>` for a full interactive lesson.

## Style

- About 300–600 words, depending on how dense the source is. Short sections with headings; tables only for comparing items across the same attributes.
- Concrete case first, then the general rule, then notation, and only if notation is needed.
- Paraphrase the source; quote at most a short phrase where the exact wording matters. Link to the source.
- Anything current (versions, CVEs, prices, rules): check it and cite it. Label guesses as guesses.
- Visual first: the picture comes before the prose explaining it. If the topic has no spatial structure, use a timeline, a before/after pair, or a table of cases.
- Voice mode: describe the picture so a listener can draw it in their head, and offer to draw it in text.
- If the user says "just explain it", skip the design-brief framing but keep the order: problem, failure, fix, name last.

## Follow-ups

- "What is X?" mid-way: answer in 2–3 lines, then connect it back to the explanation.
- "Simpler" or "I still don't get it": switch to an everyday physical analogy, drop all notation, and try a different picture rather than rewording the same one.
- "Go deeper on part N": expand only that part, using the same structure.
- If the learner wants to really own the topic, hand off to /teachme.
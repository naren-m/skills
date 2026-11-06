---
name: digital-garden-wiki
description: Maintain Naren's Jekyll digital garden and literature-notes LLM wiki. Use when Codex is asked to ingest articles/books/videos into the wiki, create or improve notes, query/summarize existing knowledge, lint backlinks and note quality, update the literature-notes submodule, run the Jekyll build, or commit/push digital garden changes in ~/Projects/naren-m.github.io.
---

# Digital Garden Wiki

Use this skill for the personal digital garden at `~/Projects/naren-m.github.io` and its `literature-notes` submodule. Treat the repo as a Jekyll publishing layer over an LLM-maintained wiki.

## First Steps

1. Read `~/Projects/naren-m.github.io/AGENTS.md`.
2. For content work, also read `literature-notes/AGENTS.md` and `literature-notes/RULES.md`.
3. Check state before editing:
   ```bash
   git status --short --branch
   git -C literature-notes status --short --branch
   ```
4. Use `rg` before creating notes to avoid duplicates.

## Task Router

- **Ingest a source:** create or update source-bound literature/research notes first; promote only durable, atomic ideas into permanent notes.
- **Create a permanent note:** write one idea in the user's own words, add useful wikilinks, and place it in `literature-notes/content/domains/...` or `literature-notes/content/people/...`.
- **Answer from the wiki:** start at `literature-notes/INDEX.md`, search with `rg`, follow related wikilinks, and answer from maintained notes before using the web.
- **Lint the wiki:** check duplicate concepts, missing front matter, orphaned important notes, broken wikilinks, stale indexes, and notes with the wrong type.
- **Publish or verify:** run Jekyll build after structural or plugin changes; preserve generated files unless the user explicitly asks to commit regenerated output.

## Core Rules

- Classify new notes before writing: `permanent`, `literature`, `research`, or `journal`.
- Do not turn highlights, quotes, transcripts, or raw captures into permanent notes directly.
- Keep source material source-bound and cited.
- Prefer updating an existing permanent note over creating a near-duplicate.
- Use wikilinks for semantic connections; folder placement is not enough.
- Keep root `_notes/` changes for site landing pages or Jekyll-specific content. Put canonical knowledge in `literature-notes/`.
- Do not revert unrelated dirty work. Treat submodule state carefully.

## Common Commands

```bash
rg "topic" literature-notes _notes
bundle exec jekyll build --trace
git submodule update --init --recursive
git -C literature-notes pull origin main
```

If local Ruby/Bundler is broken, note the issue instead of changing committed dependency files unless dependency maintenance is the task.

## References

- Read `references/repo-map.md` when locating files, understanding publishing, or touching CI/deployment.
- Read `references/workflows.md` for detailed ingest, query, lint, build, and publish checklists.

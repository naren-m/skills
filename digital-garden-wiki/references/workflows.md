# Workflows

## Ingest Source

1. Capture the source URL, title, author, publication date, and access date when available.
2. Decide note type:
   - `literature` for one source's highlights, quotations, timestamps, or summary.
   - `research` for multi-source exploration or unresolved synthesis.
   - `permanent` only for one durable idea rewritten in the user's own words.
3. Search existing notes with `rg` for the title, author, and key concepts.
4. Create or update the source note under the appropriate `literature-notes/content/media/...` path.
5. Extract durable concepts and link them to existing permanent notes.
6. Create new permanent notes only when the idea is atomic, evergreen, and not already covered.
7. Update `literature-notes/INDEX.md` only when navigation or major coverage changed.
8. Run a Jekyll build if public structure or generated site behavior may change.

## Create Permanent Note

1. Search for duplicates first.
2. Pick a concept title, not a source/chapter title.
3. Use front matter compatible with `literature-notes/AGENTS.md`:
   ```yaml
   ---
   title: "Note Title"
   date: YYYY-MM-DD
   type: permanent
   category: "Domain/Subdomain"
   tags: [tag]
   status: draft
   related: ["[[Related Note]]"]
   ---
   ```
4. Write a short core claim, explanation, and optional example or contrast.
5. Add at least two meaningful wikilinks when relevant notes exist.
6. Link back to source notes if the idea came from an ingest.

## Query The Wiki

1. Start with `literature-notes/INDEX.md`.
2. Search with `rg` across `literature-notes/` and `_notes/`.
3. Read likely permanent notes, source notes, and related landing pages.
4. Distinguish maintained wiki facts from fresh web facts if browsing is needed.
5. Answer concisely and cite local files with absolute file links when useful.
6. If the query reveals reusable synthesis, offer to create a research or permanent note.

## Lint The Wiki

Check:

- Notes without required front matter.
- Literature/research notes mislabeled as permanent.
- Permanent notes that contain raw quotes, transcripts, or unresolved brainstorms.
- Duplicate permanent concepts.
- Important notes with no meaningful links.
- Broken or inconsistent wikilinks.
- Stale `literature-notes/INDEX.md` navigation.
- CI copy commands that no longer match `literature-notes` structure.

Prefer small fixes: add links, clarify titles, split mixed notes, or create a research workbench for unsettled material.

## Verify Build

1. Confirm dependency environment.
2. Run:
   ```bash
   bundle exec jekyll build --trace
   ```
3. If local Ruby/Bundler fails, report the environment issue and compare with CI Ruby version.
4. If verification changes `Gemfile.lock`, `_includes/notes_graph.json`, `_site/`, or submodule state unintentionally, restore those generated/environment changes before finishing.

## Commit And Push

1. Check both parent and submodule status.
2. Stage only intended files.
3. Use a focused commit message.
4. Push with the GitHub identity that has access to `naren-m/naren-m.github.io`.
5. If pushing to both `main` and `master`, verify remote heads after pushing:
   ```bash
   git ls-remote --heads https://github.com/naren-m/naren-m.github.io.git main master
   ```

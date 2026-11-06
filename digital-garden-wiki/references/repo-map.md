# Repo Map

## Repositories

- Site repo: `~/Projects/naren-m.github.io`
- Canonical notes submodule: `~/Projects/naren-m.github.io/literature-notes`
- Public site: `https://naren-m.github.io`

## Site Layer

- `_notes/`: Jekyll collection that becomes public note pages.
- `_plugins/bidirectional_links_generator.rb`: converts `[[wikilinks]]`, creates backlinks, and writes graph data.
- `_includes/notes_graph.html`: D3 knowledge graph UI.
- `_includes/notes_graph.json`: generated graph data; do not commit regenerated output unless asked.
- `.github/workflows/deploy-digital-garden.yml`: GitHub Pages deployment with custom Jekyll plugins.

## Canonical Wiki Layer

- `literature-notes/content/domains/...`: permanent domain notes.
- `literature-notes/content/people/...`: permanent person notes.
- `literature-notes/content/media/...`: literature/source notes for books, articles, podcasts, videos, highlights.
- `literature-notes/content/research/...`: workbench notes and unresolved synthesis.
- `literature-notes/content/journal/...`: fleeting capture.
- `literature-notes/INDEX.md`: navigation/index overview.
- `literature-notes/AGENTS.md` and `literature-notes/RULES.md`: note classification and quality rules.

## Deployment Facts

- GitHub Pages must build through GitHub Actions because custom plugins are required.
- The workflow currently copies selected `literature-notes` directories into `_notes/` during CI.
- Remote branches `main` and `master` may both exist; confirm desired target before publishing.
- Deployment triggers are defined in `.github/workflows/deploy-digital-garden.yml`; check that file before assuming which branch deploys.

## Build Notes

- Preferred build command: `bundle exec jekyll build --trace`.
- CI uses Ruby 3.3.
- Local macOS system Ruby may be too old; do not let local verification rewrite `Gemfile.lock` accidentally.

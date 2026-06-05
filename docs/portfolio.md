# portfolio — executive summary

**One-liner:** The public index and starting point for all these projects — an interactive, self-contained map of what each repo is and how they fit together.

## What it provides
A single public page (`index.html`) listing every repository — public and private — with
search, public/private filtering, tag chips, and a by-language chart. Repo data is an embedded
S-expression; the style is inlined with a provenance header; ECharts is vendored. A `docs/`
directory holds an executive summary for each repo (this directory), so the public page can
surface *what each project does* even when the repo itself is private.

## Strengths
- **Self-contained & portable** — opens from GitHub Pages or `file://`, no server, no CDN.
- **One public entry point** for an otherwise-private ecosystem.
- **Convention source of truth** — `tools/mdpage.py`, `style/*.css`, and the `{{name}}`
  placeholder + embedding/provenance conventions live here and are reused by every repo.

## Weaknesses / limitations
- Summaries are hand-curated and can drift from the repos they describe.
- Links to private repos 404 for anyone without access (by design).
- Deliberately "leaks" capability summaries of private work — appropriate only because that
  exposure is intended.

## Why you'd use it
As the front door: to see, at a glance, every project, what it does, and how the pieces relate
— then jump to whichever repo (or its rendered README) matters.

## How it relates to the other projects
It indexes and links to all of them, and each repo links back here as its top-level reference.
It documents the shared conventions (placeholders, embedding, README→web rendering via
`tools/mdpage.py`) that the whole portfolio follows.

---
*Executive summary. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

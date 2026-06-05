# gmail-utility — executive summary

**One-liner:** A spec-first CLI for pulling your entire Gmail into a local, searchable archive — SQLite metadata plus standard `.eml` files with a paranoid two-stage trash — now wired to a YBS/dagsmith build system that orchestrates its 24-step, 11-phase implementation.

## What it provides
- A complete design and orchestrated build pipeline for a Gmail archiver: bulk download via the Gmail REST API (batch requests) into a local archive, with metadata-only SQLite (plus an FTS5 full-text index, no BLOBs) alongside message bodies stored as universal `.eml` files.
- Attachment extraction with SHA256 deduplication and reference counting, so identical attachments are stored once.
- A safe, reversible cleanup workflow — delete → local trash → review → purge — designed on two databases (`gmail.db` active, `gmail-trash.db` trash) with undelete and dry-run support.
- A **YBS build system** under `systems/gmail-utility/`: a spec, 24 discrete step files across 11 phases, and an explicit dependency graph (`STEPS_ORDER.txt`) that maps to parallel execution rounds, driven by a **dagsmith**-style `.dagsmith.json` executor configuration.
- Search over the archive (sender/subject/label/date filters) and an intended Claude Code skill integration for conversational email management.

## Strengths
- **Clear, opinionated architecture**: metadata-only SQLite + on-disk `.eml` keeps the database small and fast while leaving content in a portable, future-proof format.
- **Safety-first design**: trash-before-delete, undelete, dry-run, read-only Gmail scope, and a hard rule against destructive operations on live mail. Data directories live outside the repo to avoid leaking mail into git/tar/backups.
- **Build is now executable, not just documented**: the ~40 KB proposal and ~50-step plan have been distilled into discrete YBS steps with a dependency DAG, so the implementation can be orchestrated (and parallelized) by dagsmith rather than hand-walked.
- **Reconciliation-based sync** (set difference rather than a checkpoint table) keeps the sync model simple and robust.

## Weaknesses / limitations
- **Pre-implementation**: this remains the key caveat. The runtime functionality is not built yet — only a ~123-line `click` CLI skeleton exists with every command printing "not yet implemented", and the `api/`, `storage/`, `sync/`, `trash/`, and `utils/` packages are empty `__init__.py` stubs. The YBS steps describe the work; they have not yet been executed against the code.
- **No tests yet** beyond an empty scaffold, so the safety guarantees are specified but unproven in code. `SESSION_STATE.md` still lists Phase 0 as "NOT STARTED."
- **Setup friction**: requires a Google Cloud project, Gmail API enablement, and user-provided OAuth credentials before first use; assumes Python 3.11+ and pyenv.
- **Single-account / local-only** in scope; no multi-account, server, or sync-back-to-Gmail story (by design it stays read-only against Gmail).
- **Version-locked at 0.1.x**, signaling it is explicitly not yet ready for general use.

## Why you'd use it
Use it when you want a durable, self-owned, locally searchable archive of your Gmail and a safe way to declutter — bulk-deleting old promotions or newsletters without trusting an irreversible action against your live inbox. The `.eml` + SQLite combo is attractive if you value portable, tool-agnostic storage and full-text search you control. Today it is best read as a reference spec and a ready-to-run build plan rather than a finished tool — but the YBS system means going from spec to working code is now an orchestrated process rather than a from-scratch effort.

## How it relates to the other projects
gmail-utility is the Gmail-specific, local-archive counterpart to **gws** (the broader Google Workspace CLI), sharing a Google-API domain and overlapping auth/data-handling philosophy. It now carries its own **ybs** system — the portfolio's spec/step build methodology — turning its proposal and implementation plan into discrete, dependency-ordered steps. Those steps are executed by a **dagsmith** build orchestrator (configured here via `.dagsmith.json`), which resolves the step DAG and runs rounds of work in parallel. As a clean, scoped CLI over a well-defined data store, its eventual local archive is a natural data source for agentic systems in the portfolio, including **memory** (agentic memories), and its planned Claude Code skill hook aligns it with that conversational-tooling ecosystem.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

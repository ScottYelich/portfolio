# gmail-utility — executive summary

**One-liner:** A CLI tool to pull your entire Gmail down into a local, searchable archive — SQLite metadata plus standard `.eml` files — with a deliberately paranoid two-stage trash system so cleanup never loses mail by accident.

## What it provides
- Bulk download of Gmail messages via the Gmail REST API (batch requests) into a local archive.
- Local storage split for speed and portability: SQLite holds metadata plus an FTS5 full-text search index (no BLOBs), while message bodies live as standard `.eml` files readable by any mail client.
- Attachment extraction with SHA256 deduplication and reference counting, so identical attachments are stored once.
- A safe, reversible cleanup workflow — delete → local trash → review → purge — built on two databases (`gmail.db` active, `gmail-trash.db` trash) with undelete support.
- Search over the archive (e.g. `from:`, `subject:`, label/date filters) and an intended Claude Code skill integration for conversational email management.

## Strengths
- **Clear, opinionated architecture**: metadata-only SQLite + on-disk `.eml` keeps the database small and fast while leaving content in a universal, future-proof format.
- **Safety-first design**: trash-before-delete, undelete, dry-run, read-only Gmail scope, and a hard rule against destructive operations on live/pre-existing mail. Data directories live outside the repo to avoid leaking mail into git/tar/backups.
- **Thoroughly specified**: a ~40 KB technical proposal and a ~50-step, 11-phase implementation plan with checkpoints and tests, plus a session-state tracker for resumable, incremental development.
- **Reconciliation-based sync** (set difference rather than a checkpoint table) keeps the sync model simple and robust.

## Weaknesses / limitations
- **Pre-implementation**: this is the project's most important caveat. Despite extensive docs, essentially no functionality is built yet — only a ~123-line `click` CLI skeleton exists; the `api/`, `storage/`, `sync/`, `trash/`, and `utils/` packages are empty `__init__.py` stubs, and the test suite is empty. Session state lists Phase 0 (project setup) as "NOT STARTED."
- **No tests yet** beyond an empty scaffold, so the safety guarantees are specified but unproven in code.
- **Setup friction**: requires a Google Cloud project, Gmail API enablement, and user-provided OAuth credentials before first use; assumes Python 3.11+ and pyenv.
- **Single-account / local-only** in scope; no multi-account, server, or sync-back-to-Gmail story (by design it stays read-only against Gmail).
- **Version-locked at 0.1.x**, signaling it is explicitly not yet ready for general use.

## Why you'd use it
Use it when you want a durable, self-owned, locally searchable archive of your Gmail and a safe way to declutter — bulk-deleting old promotions or newsletters without trusting an irreversible action against your live inbox. The `.eml` + SQLite combo is attractive if you value portable, tool-agnostic storage and full-text search you control. Today, though, it is better read as a reference spec than a tool you can run.

## How it relates to the other projects
gmail-utility is the Gmail-specific, local-archive counterpart to **gws** (broader Google Workspace tooling), and the two share a Google-API domain and likely overlapping auth/data-handling philosophy. It echoes the portfolio-wide pattern of spec-first development seen in **ybs**-built projects (gws, yobro): a detailed proposal and step-by-step implementation plan precede code, with session-state tracking for resumable, agent-friendly work. As a clean, scoped CLI over a well-defined data store, its local archive could serve as a data source for agentic systems in the portfolio — **memory** (durable memories), **mind**/**murphy** (LLM processing/execution), and **agent** (macOS work-queue worker) — and its Claude Code skill hook aligns it with that conversational-tooling ecosystem.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

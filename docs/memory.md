# memory — executive summary

**One-liner:** A passive, file-based memory layer for agentic systems that turns every Murphy turn, Agent job, dagsmith step, and shell command into a linked Obsidian-compatible markdown note — without any tool needing to know it exists.

## What it provides
- A Zettelkasten-style knowledge store at `~/.memory/`, where each interaction is one atomic markdown file (`.md`) with YAML frontmatter and `[[id]]` wikilinks.
- Decoupled "importers" (Murphy, Agent, dagsmith, Shell) that read each tool's *existing* output format after the fact and create memories — zero coupling, so if Memory breaks nothing else breaks.
- A planned CLI (`memory collect | search | show | thread | session | recent | related | tags`) for idempotent collection and traversal of memories by source, session, thread, tag, or link.
- An Obsidian-compatible vault: open `~/.memory/` in Obsidian to browse the graph, follow links, and query with Dataview.

## Strengths
- Zero-coupling design: tools write their normal output and never import or call Memory, making the whole stack resilient and independently testable.
- Source of truth is plain markdown + YAML — human-readable, diffable, portable, and tool-agnostic (no database required; SQLite only as optional cache).
- Atomic, ID-linked memory units (one turn / command / job / step) compose into threads and sessions, enabling clean graph traversal.
- Idempotent collection avoids duplicates by checking existing IDs.
- Clean separation of concerns: Memory stores; Mind (a sibling) interprets.

## Weaknesses / limitations
- Status is "design complete, implementation pending" — the CLI, importers, and store are specified but not yet built, so today it is documentation rather than working software.
- Passive by design: it does no thinking, learning, or summarization on its own; value depends on Mind being built and run.
- Dual link representation (frontmatter `links:` array + body `[[id]]` wikilinks) must be kept in sync manually/by convention, a likely source of drift bugs.
- File-per-memory at scale (potentially many thousands of notes) may stress filesystem and Obsidian performance and make search/traversal slower without the optional cache.
- Tight conceptual reliance on specific sibling tool output formats (JSONL, job dirs, event logs) means importers are coupled to those schemas even though the tools aren't coupled to Memory.

## Why you'd use it
Use Memory when you want a durable, inspectable, plain-text record of everything your agentic tool stack does — and a substrate that downstream intelligence can mine for patterns — without retrofitting logging or instrumentation into the tools themselves. It is the system of record for the agent ecosystem: capture now, understand later.

## How it relates to the other projects
Memory sits downstream of the execution tools and upstream of analysis. Its importers consume outputs from **murphy** (JSONL turn events), **agent** (job directories in the work-queue), and **dagsmith** (build step event logs), plus shell history — none of which depend on Memory in return. **mind** is the intelligence layer: it reads the memory store and writes `pattern`/`observation` memories back into the same vault, closing the loop. **mlx-router** has no direct relationship (Murphy talks to it, not Memory). Like much of the portfolio (e.g. **saixha**'s code-as-data ethos), Memory leans on a simple, transparent, file-native representation as its foundation. Built in Swift, consistent with sibling tools like murphy and agent.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

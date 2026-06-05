# ybs — executive summary

**One-liner:** A spec-and-step build methodology that lets AI agents construct whole systems autonomously, with traceability and verification baked in.

## What it provides
YBS (Yelich Build System) is a **methodology + framework** for defining software as a graph
of specifications and executable build steps that an AI agent can run end-to-end. It is
configuration-first (a Step 0 collects all config up front into `BUILD_CONFIG.json`), then
proceeds through steps without prompting. Every step carries explicit verification criteria
and traceability links from code back to requirements. The 2.0 direction models all spec/step
artifacts as atomic **S-expression `.ybs` graph nodes** linked by GUIDs, so quality is
provable from graph structure rather than prose.

## Strengths
- **Autonomous, repeatable builds** — agents execute without hand-holding after Step 0.
- **Traceability & verification** are first-class (code ↔ spec links, per-step checks, retry limits).
- **Language- and system-agnostic** framework; reusable templates and tools.
- The S-expression graph model makes specs machine-checkable.

## Weaknesses / limitations
- Up-front rigor (specs before code) is heavier than ad-hoc coding for small tasks.
- The 2.0 S-expression rework currently lives on `develop`, unmerged — two models coexist.
- Effectiveness depends on disciplined step authoring; a vague step yields vague builds.

## Why you'd use it
When you want an AI agent to build (or rebuild) a system **reproducibly and verifiably** from
a written specification, rather than improvising — especially across multiple builds or agents.

## How it relates to the other projects
YBS is the **methodology backbone** of the portfolio. Several systems are specified *in* YBS
(`gws`, `murphy`, `saixha`, `yobro` all carry `.ybs` spec/step files). `dagsmith` orchestrates
multi-step builds and complements YBS's step model. `saixha`'s S-expression substrate shares
the same "code = data" philosophy as YBS 2.0's `.ybs` graph. In short: YBS defines *how*
things get built; the other repos are *what* gets built (often through it).

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

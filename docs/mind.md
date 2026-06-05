# mind — executive summary

**One-liner:** The intelligence layer that reads your memories, learns "what usually happens next," and writes back human-readable patterns — Memory stores what happened, Mind understands what it means.

## What it provides
Mind is a planned on-demand (non-daemon) processor that sits on top of the Memory store (`~/.memory/memories/`). It reads accumulated memories, maintains a lightweight Bayesian behavioral model (transition probabilities, co-occurrence matrices, temporal weights), and uses an LLM to turn the top statistical patterns into first-class pattern/observation memories written back to the same store.

- **Statistical core:** simple count-and-normalize probability tables answering "given what just happened, what usually happens next?" — updated per-memory in microseconds, stored as plain JSON at `~/.mind/model.json`.
- **LLM interpretation:** feeds the strongest patterns to Murphy (via mlx-router) to generate readable observations with confidence scores and evidence links.
- **Memories in, memories out:** outputs are normal markdown memories (`kind: pattern`, `kind: observation`, `source: mind`) — searchable, linkable, visible in the Obsidian graph.
- **CLI surface:** `observe`, `learn`, `suggest --context <id>`, `patterns`, `profile`, `explain <id>`.

## Strengths
- **Deliberately simple.** Rejects neural/"anima engine" complexity in favor of probability tables; the entire learning algorithm is count, normalize, decay — trivially debuggable and microsecond-fast.
- **Zero coupling.** Murphy, Agent, dagsmith, and Memory don't know Mind exists. It only reads/writes files by filesystem convention, so if Mind breaks, nothing else does.
- **Clean separation of concerns.** Stats find the patterns; the LLM only supplies language. Storage is Memory's job; computation is Mind's.
- **Inspectable artifacts.** Both the model (JSON) and the outputs (markdown with evidence chains) are human-readable and grep-friendly.
- **Flexible execution.** Run manually, on a schedule, post-collection, or as a watch loop — no always-on process required.

## Weaknesses / limitations
- **Not implemented.** Status is "design complete, implementation pending." This is a specification/architecture repo (only README + CLAUDE.md), not working software.
- **Cold-start dependency.** Useless until Memory is populated with enough data to learn from.
- **Runtime dependencies for the LLM path.** Natural-language observation generation needs Murphy and mlx-router running locally; without them only raw statistics are available.
- **Single-user / single-machine assumptions.** Built around local home-directory paths and one person's behavioral profile; no multi-user or distributed story.
- **Naive learning model by design.** Counting/normalization will not capture higher-order or long-range structure; the simplicity that is a strength is also a ceiling.

## Why you'd use it
Use Mind when you have a growing Memory store of agent/tool/shell activity and want it to become more than an archive — to surface recurring workflows, preferences, and "next-action" predictions that downstream tools (like Murphy) can act on proactively. It is the right tool when you value a transparent, debuggable statistical model over an opaque neural one, and want insights expressed as ordinary, linkable memories rather than a black-box service.

## How it relates to the other projects
Mind sits directly downstream of **memory**: it reads from and writes to the same `~/.memory/memories/` store, acting as the computation layer to Memory's storage layer. For natural-language interpretation it calls **murphy** (the Swift LLM processing/execution engine) over an OpenAI-compatible HTTP interface routed through **mlx-router** (local MLX inference) — the same path Murphy itself uses. **agent** (the macOS work-queue daemon) may dispatch `mind observe` as a scheduled job but does not otherwise depend on Mind. Upstream tools whose output becomes memories — Murphy (JSONL events), Agent (job directories), and **dagsmith** (DAG build/event logs) — feed Mind indirectly via Memory importers, with zero coupling. Implementation-wise it shares the Swift stack and local-LLM philosophy of Murphy, Agent, and dagsmith.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

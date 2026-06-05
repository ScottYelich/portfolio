# saixha — executive summary

**One-liner:** An S-expression AI shell (pronounced "Sasha") where the LLM, a Lisp interpreter, and Swift built-ins are all in-process evaluators — and forking out to a real command is the exception, not the rule.

## What it provides
saixha is the design for an interactive macOS shell where evaluation happens in-process by default and S-expressions are the native substrate (code = data = pipe format). Distinct input prefixes route to distinct evaluators: `/cmd` (Swift built-in), `!cmd` (force shell exec), `!!cmd` (shell exec whose stdout is piped into LLM context), `?text` (one-shot LLM query), `:text` (stateful murphy conversation), `@type job.sh` (agent enqueue), `$(expr)` (inline Lisp), and bare text falling back to the LLM. The signature feature is the `!!` bridge: run a real command and its output is silently added to the conversation, so the next LLM question already has the data — no copy-paste. It also specifies a dependency-free Swift-native Lisp interpreter (~900 lines, scoped as a config/spec DSL), built-in commands for the agent job queue, context save/load, aliases, and mlx-router model tiers.

## Strengths
- Coherent, well-articulated design philosophy ("fork is the escape hatch, not the default") borrowed cleanly from `/bin/sh` semantics.
- The `!!cmd` context bridge is a genuinely useful idea: it fuses deterministic shell output with non-deterministic LLM reasoning without manual copy-paste.
- S-expression-as-pipe-format gives typed, self-describing, AND executable inter-process data — a real step beyond text or JSONL.
- Clean ecosystem boundaries: it calls murphy as a function, reads agent's queue dirs, and routes inference through mlx-router rather than re-implementing any of them.
- Disciplined constraints: no third-party Swift packages, no direct `api.anthropic.com` calls, no terminal emulator, no embedded agent loop.

## Weaknesses / limitations
- Essentially a scaffold at v0.1.0: the REPL is not implemented. Source is an 11-line `main.swift` and a 6-line test — none of the documented behavior exists in code yet.
- All the value is currently in docs/specs (architecture, naming etymology), not in a runnable artifact.
- Tightly coupled to a specific macOS 26 / Swift 6 stack and a bespoke sibling ecosystem (murphy, agent, mlx-router); not portable or standalone.
- The embedded Lisp is deliberately limited (no TCO, GC, or continuations); anything needing full Scheme requires swapping in s7.
- Heavy reliance on local conventions (`~/ai/bin`, `$AGENT_HOME/queue/`, mlx-router tiers) means it only "works" inside its author's environment.

## Why you'd use it
You'd reach for saixha when you want a single interactive prompt that blends ordinary shell work, structured Lisp scripting, and an always-available LLM that can see your real command output — without context-switching to a separate chat window or pasting logs. It is the human-facing front door to an AI-agent ecosystem: inspect agent jobs, ask murphy stateful questions, and pipe shell reality into the model, all from one REPL. Today, though, it is a blueprint to build from, not a tool to run.

## How it relates to the other projects
saixha is the interactive shell layer of a larger AI-agent ecosystem. It calls **murphy** (the LLM processing/execution engine) as an in-process function with a clean S-expression I/O contract for `:` and `?` queries. It talks to **agent** (the macOS work-queue daemon) by reading its queue directories and shelling out to its CLI via `@type job.sh`, never embedding the agent loop. LLM inference routes through **mlx-router** (local MLX inference) via murphy and the `/model` tier selector. **dagsmith** builds the ecosystem, and the build methodology traces to **ybs** (the spec/step S-expression `.ybs` graph), which is also the shared philosophical root of "S-expression as the universal substrate." **laniakea** owns the `~/ai/bin/` script layer that saixha sits alongside, and **memory** consumes agent job dirs that saixha can inspect. The whole set is indexed from the public **portfolio**.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

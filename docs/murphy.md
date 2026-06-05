# murphy — executive summary

**One-liner:** A single-shot Swift AI agent engine for macOS — prompt in, structured JSONL events out, exit code — a disciplined worker that does one agent loop and gets out of the way.

## What it provides
Murphy takes a prompt, runs one LLM-plus-tools agent loop, streams every action as canonical JSONL events on stdout, and exits with a structured code. It ships six built-in tools (`read_file`, `write_file`, `edit_file`, `list_files`, `search_files`, `run_shell`) and auto-discovers external tools that respond to `--schema`. A single OpenAI-compatible HTTP adapter is its only provider interface, so all model-specific translation (Anthropic, Apple Foundation Models, local Qwen/Llama/Hermes) is delegated to mlx-router and Murphy itself stays provider-agnostic. It runs non-interactively (`murphy -p "..."`) and is designed to be invoked as a subprocess by an orchestrator.

## Strengths
- Clean separation of concerns: a worker, not an orchestrator — never retries across runs, escalates models, or manages multi-step builds.
- Fully observable: 19 event types covering the whole lifecycle (session, rounds, text deltas, tool calls, errors, cancellation) as flat one-object-per-line JSONL.
- Provider-agnostic by design — one HTTP adapter, zero Anthropic/OpenAI-shaped types leaking into the engine.
- Security by default: path sandboxing, deny-by-default file access, symlink/path-traversal prevention, sandboxed shell execution.
- Swift 6 with strict concurrency and no third-party dependencies; v2 binary is built and installed with 772 tests passing.
- Fast, predictable failure — connection errors exit immediately with a structured code, leaving the decision to the caller.

## Weaknesses / limitations
- macOS-only, and the deploy step is fragile: copying the binary invalidates the ad-hoc code signature and it must be re-signed or it silently dies (`zsh: killed`).
- The shipping artifact is v2; v3, v4, and v5 are specs/plans, not running code, so the headless canonical-event engine described in the README is partly aspirational.
- Repo carries significant clutter — multiple historical build-spec trees (v1–v5) plus loose debugging files (MLX tool-calling issue notes, quick-fix checklists, test scripts) at the top level.
- Useful only in concert with mlx-router for inference; on its own it cannot reach Anthropic, Apple FM, or local models.
- No UI, REPL, or interactive mode (by design) — not meant for direct human conversation.

## Why you'd use it
Use Murphy when you need a reliable, scriptable execution unit that runs exactly one AI agent task and reports everything it did in a machine-readable stream. It is the right tool when an orchestrator (or a human) wants to dispatch work, watch structured events, and make retry/escalation decisions externally — rather than embedding that logic in the worker.

## How it relates to the other projects
Murphy is the middle layer of a three-tool stack: **agent** (the macOS work-queue daemon) dispatches jobs, **dagsmith** (the DAG orchestrator) reads YBS steps and calls Murphy as an executor subprocess, and Murphy runs the actual agent loop. Downstream, Murphy speaks only OpenAI-compatible HTTP to **mlx-router**, which translates every provider (local MLX models, Anthropic, Apple Foundation Models, OpenAI). Its JSONL output is consumable by **dagsmith** and importable into **memory** (and onward to **mind** for pattern detection). Murphy itself is built with the **ybs** spec/step methodology, and shares the laniakea-style `~/ai/bin/` deployment convention with the rest of the portfolio.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

# dagsmith — executive summary

**One-liner:** `make` for AI work — a dependency-aware DAG orchestrator that dispatches markdown build steps to pluggable AI executors, except the build graph can rewrite itself while it runs.

## What it provides
dagsmith reads structured step files (markdown), resolves their dependency graph, and dispatches ready steps to pluggable executors (Murphy, Claude Code, aider, shell scripts — anything that takes markdown in and returns structured JSON out). It is purely the *orchestrator*: it schedules, dispatches, and tracks state, but executes nothing itself. Key capabilities include topological scheduling with parallel dispatch of independent steps, a runtime-mutable DAG (planners, executors, or humans can inject/modify steps mid-build), an entirely filesystem-based state protocol (event log, DONE files, questions, control signals), and crash recovery that resumes from the last checkpoint. It ships a Swift CLI with 15 subcommands (run, plan, status, pause/resume, answer, interactive REPL, attach), an HTTP REST API, and an MCP server for Claude Code integration. It natively understands the YBS step/dependency format, plus single-file and directory input formats via auto-detection.

## Strengths
- **No LLM in the scheduler** — scheduling is pure graph math, so it is deterministic, free (zero tokens to plan), and fast; only the executors spend tokens.
- **Filesystem-native state** makes crash recovery essentially free and lets any external tool read/inspect build state (events, BUILD_STATUS.md, questions/, control/).
- **Loosely coupled, language-agnostic executors** — subprocess "markdown in, JSON out" contract means executors can be any tool in any language (Murphy, Claude Code, CrewAI/LangGraph agents, plain scripts).
- **Mutable DAG with a human-in-the-loop protocol** — async questions, answers, pause, priority changes, and runtime step injection are first-class, unlike static schedulers (make/Airflow).
- **Self-hosting / dogfooded** — dagsmith ships its own YBS build definition (it can build itself), and has a no-Xcode test runner.

## Weaknesses / limitations
- **macOS-first.** Swift was chosen for ecosystem alignment with Murphy; Linux runs but the toolchain/ecosystem is thinner and less tested, and the static binary advantage shrinks there.
- **Documentation status is inconsistent.** The README presents all features as complete with 58 tests passing, while CLAUDE.md describes an earlier state (24 tests, orchestrator/REPL/HTTP/MCP "not yet implemented"). Treat the precise maturity of the orchestrator loop and frontends as needing verification before relying on them.
- **Niche by design.** It is the wrong tool for one-off tasks (use an executor directly) or exploratory/unknown-step work (use an emergent multi-agent system); its value only appears once a structured, repeatable plan exists.
- **Smaller contributor pool** for a Swift CLI tool versus Go/Python equivalents; explicitly framed as a personal/small-team project.
- **HTTP/MCP frontends are secondary.** The core is headless-first; network frontends were backlog items and add external dependencies.

## Why you'd use it
Reach for dagsmith when you have a *known, structured plan* of AI-driven build steps with real dependencies and want to run it reliably, repeatably, and in parallel. It shines for builds that must survive crashes, mix heterogeneous executors (Murphy + Claude + scripts) in one graph, expose inspectable state to other tooling, and support async human-in-the-loop decisions. Choose something else for ad-hoc single tasks or open-ended "figure out what's wrong and fix it" exploration where the steps aren't known up front.

## How it relates to the other projects
dagsmith sits at the center of the build-automation stack as the **orchestrator** role, distinct from planners and executors. It consumes the **ybs** spec/step methodology natively — STEPS_ORDER.txt and its S-expression-derived dependency graph are dagsmith's primary input format, and ybs acts as the planner that produces the DAG. It dispatches work to executors, most directly **murphy** (the Swift LLM execution engine, with which it deliberately shares the Swift ecosystem, types, and subprocess patterns), and equally to **agent** (the macOS work-queue daemon / AI worker loop), Claude Code, or any script. Conceptually it pairs with **mlx-router** when executors route to local MLX inference, and its filesystem event/state protocol is a natural producer/consumer alongside **memory** (persistent memories for agentic systems) and **mind** (agentic processing). It is a foundational piece of the broader portfolio that also includes ybs-built applications such as **gws**, **yobro**, and **gmail-utility**.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

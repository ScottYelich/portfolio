# agent — executive summary

**One-liner:** Drop a file into a folder and it runs — a no-polling macOS daemon that turns directories into a durable, concurrency-controlled work queue.

## What it provides
- A persistent macOS LaunchAgent (`KeepAlive`) that watches typed `drop/<handler>/` directories via `DispatchSource`/kqueue and executes work the instant a file appears — no polling, no scheduler.
- A filesystem-as-database job state machine (`inbox → running → done | failed`) where every job is a directory containing a JSON manifest, the payload, captured stdout/stderr logs, and sidecar status files.
- Execution primitives only: concurrency limits, LockKey mutual exclusion, per-job timeouts, heartbeat monitoring, and graceful drain for zero-loss binary upgrades.
- Fully config-driven job types — handlers are declared in `~/.config/agent/handlers.json`; adding a new job type needs only a config edit plus `agent init`, never a binary change.
- A CLI for the full lifecycle: `init`, `loop`, `enqueue`, `status`, `logs`, `cancel`, `retry`, `purge`, `drain`. Status reads the filesystem directly and never consumes a worker slot.

## Strengths
- Event-driven and efficient: kqueue watchers instead of polling loops; correctness comes from directory scans, not event delivery.
- Durable and inspectable by design — state lives entirely on disk as JSON + sidecar files, so jobs survive restarts and can be examined with ordinary shell tools.
- Clean architecture: Swift 6 with strict (`complete`) concurrency, zero third-party dependencies, and a deliberate decoupling where `AgentLoop` and `JobRunner` never import each other (wired only through a `JobExecutor` protocol).
- Mechanism, not policy: the binary has no hard-coded job logic, making it a reusable substrate that any CLI tool or AI worker can plug into.
- Graceful drain enables safe in-place upgrades — SIGTERM stops intake, lets in-flight jobs finish, then lets launchd relaunch the new binary.

## Weaknesses / limitations
- Single-machine and macOS-only (macOS 26.0+, Swift 6.2+) — not distributed, not portable to Linux, no iOS/visionOS targets by design.
- Not a scheduler: jobs run when dropped, never on a cron/time basis; scheduling must come from an external system.
- Deliberately minimal — no HTTP intake, no built-in retry policy beyond attempts, no job logic of its own; real value depends on the handlers and engines wired in around it.
- Early-stage (v0.x; README describes v1 as `exec`-handler-only) with the broader feature set staged through external YBS/dagsmith builds.
- The on-disk state machine relies on filesystem atomicity conventions (LockKey mkdir mutexes, tmp-staging), tying durability and correctness to local filesystem semantics.
- Requires manual ad-hoc codesigning after each binary copy on macOS, adding operational friction to upgrades.

## Why you'd use it
Reach for agent when you want a dead-simple, reliable local execution substrate on a Mac: a place to drop work and trust it will run exactly once, with concurrency caps, locks, timeouts, and a clear audit trail on disk. It is ideal as the worker-loop backbone for an AI or automation pipeline where the intelligence lives elsewhere and you just need a robust queue that survives reboots and upgrades without losing or double-running jobs.

## How it relates to the other projects
agent is the execution backbone of a larger local-AI ecosystem. It runs the queue, but the work it executes typically comes from **murphy**, the LLM processing/execution engine that supplies the actual agent-job logic. **dagsmith** sits above it, orchestrating multi-step DAG builds — agent's own new features are even built this way, defined as YBS step files. **memory** reads agent's job directories (via an AgentImporter) to harvest memories for agentic systems, and **mlx-router** provides the local LLM inference backend those jobs call into. agent shares the portfolio's build philosophy with **ybs** (the spec/step methodology used to build agent itself) and deploys alongside **laniakea**-managed scripts into the shared `~/ai/bin/` local toolchain.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

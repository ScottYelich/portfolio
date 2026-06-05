# laniakea — executive summary

**One-liner:** The plumbing layer of a personal AI supercluster — a kit of Python and shell scripts that turn a single Apple Silicon Mac into a self-hosted LLM, vision, and inference stack reachable across the LAN.

## What it provides
- A versioned source-of-truth repo whose `./install` script deploys command-line tools into a `~/ai/bin/` runtime (copy or symlink mode, all-at-once or one tool at a time).
- An MLX-based local LLM stack for Apple Silicon: tools to start, stop, hot-swap, and route between model tiers (`mlx`, `mlx-daemon`, `mlx-router`, `mlx-query`), with an OpenAI-compatible router that dispatches requests to the right model by keyword/alias/prefix.
- Vision tooling: CLI image queries and persistent fast/deep VLM servers, plus `img-catalog` for bulk image description, full-text search, and NSFW flagging backed by SQLite/FTS5.
- Glue and operations utilities: persistent-shell daemons (`cgate` named-pipe gate, `shed` Unix-socket exec daemon), HuggingFace download/test helpers, thin LLM clients (`llm-mlx`, `llm-claude`, `llm-murphy`), a benchmark suite (context, KV-cache, model, speculative), plus extras like SearXNG, embeddings, TTS/voice, and image generation.

## Strengths
- Clear, enforced source boundary: the repo owns Python/shell scripts and config templates only; Swift binaries and the canonical mlx-router suite live in sibling repos, keeping responsibilities crisp.
- Pragmatic, hardware-aware design tuned to a known machine (M3 Ultra, 256 GB), with documented port/model/RAM assignments that make the running stack legible.
- Low-friction deploy model: a single `install` script, symlink mode for live development, and config templates that keep machine-specific settings out of version control.
- Good documentation discipline — README plus per-tool docs and design notes (router plans, unified node format, MLX manager).

## Weaknesses / limitations
- Effectively single-machine and Apple-Silicon/MLX-bound; not portable to non-Mac or non-unified-memory hardware without rework.
- Heavy implicit dependencies on a large local model cache (~200 GB+), HuggingFace access, and specific Python/runtime versions (e.g., a python3.12 vs. pyenv mlx-vlm version pitfall called out in the docs).
- It is a loose toolbox of scripts rather than a single cohesive application — no unified CLI, test suite, or packaging; reliability rests on operator knowledge of ports and conventions.
- The mlx-router suite is mirrored here but developed elsewhere, so this copy can drift from its upstream source if syncs are skipped.
- Personal infrastructure: configuration assumes one operator's environment and naming, limiting out-of-the-box reuse by others.

## Why you'd use it
Use laniakea when you want to run capable LLMs and vision models entirely on your own Apple Silicon hardware and expose them to local clients and agents over the LAN — for cost control, privacy, low latency, or offline operation — rather than relying on hosted APIs. It is the foundation the rest of the portfolio's agentic tooling sits on.

## How it relates to the other projects
Laniakea is the infrastructure floor beneath the author's agentic stack. Its `mlx-router` provides the local inference endpoint that **murphy** (the LLM execution engine) and other clients call; the canonical router/`mlx` source lives in the **mlx-router** repo and is synced here for deployment. Higher layers build on this foundation: **ybs** supplies the spec/build methodology, **dagsmith** orchestrates build steps as a DAG, **murphy** executes them, and **agent** runs an asynchronous macOS work queue — all ultimately backed by the local inference laniakea stands up. **memory** and **mind** capture and analyze activity across the system, and **gws**/**gmail-utility** plug in as external tools. In short: ybs → dagsmith → murphy → mlx-router for the build/execute/inference path, with agent feeding async jobs and memory/mind observing — and laniakea is the layer that makes the local models and daemons actually run.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

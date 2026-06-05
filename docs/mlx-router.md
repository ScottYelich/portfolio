# mlx-router — executive summary

**One-liner:** A thin, batteries-included wrapper that turns any Apple Silicon Mac into a private, OpenAI-compatible LLM endpoint backed by MLX.

## What it provides
- An OpenAI-compatible local inference server (`/v1/chat/completions`, `/v1/models`) running at `http://localhost:8080`, so existing OpenAI SDK / curl clients work unchanged with `api_key="not-needed"`.
- Native Apple Silicon (M1–M5) inference via Apple's MLX and `mlx-lm`, with all computation and data staying on the local machine.
- Convenience tooling: an interactive `install.sh`, plus helper scripts to start the server (`start-server.sh`), chat interactively (`chat.sh`), and pre-download models (`download-model.sh`).
- Access to 1000+ 4-bit-quantized models from the Hugging Face `mlx-community` org, downloaded on first use and cached locally (default `~/.mlx-models`); models are never committed to the repo.
- Simple `config.env`-based configuration of host, port, max tokens, default model, and model storage directory.

## Strengths
- Genuinely zero-friction local setup: one installer, sensible defaults (Llama 3.2 3B), and a hard system-check gate (macOS 14+, arm64).
- Drop-in OpenAI compatibility means it slots under any tooling already speaking that API with no client code changes.
- Fully local and private — no auth, no outbound calls at inference time, good for sensitive workloads and offline use.
- Lean and honest in scope: it's an explicit wrapper around `mlx-lm`, not a reimplementation, so it inherits upstream model support and performance.

## Weaknesses / limitations
- Thin by design: the heavy lifting is `mlx-lm`; this repo is essentially shell glue plus docs, so it adds little beyond ergonomics and conventions.
- Apple-Silicon-only and macOS-14+-only — no Intel, Linux, or non-Mac path whatsoever.
- "Router" is aspirational at this stage: there is no evidence of multi-backend routing, load balancing, model-aware dispatch, or queueing — it serves one model per server process.
- No authentication, rate limiting, or TLS; safe only on a trusted local/LAN boundary.
- Defaults bind to localhost and assume a single user; concurrency, observability, and production hardening are out of scope.
- First-response latency and large RAM requirements (7B ≈ 16GB, 70B ≈ 64GB+) are inherent to local inference.

## Why you'd use it
Reach for mlx-router when you want a private, cost-free LLM endpoint on a Mac that any OpenAI-compatible client can hit immediately — for local development, offline experimentation, privacy-sensitive prompts, or as the cheap inference backend for other tools in this portfolio. Choose it over a hosted API when data locality, zero marginal cost, and Apple Silicon performance matter more than scale, multi-tenancy, or operational guarantees.

## How it relates to the other projects
mlx-router is the local inference substrate for the agentic and LLM-driven projects in the portfolio. murphy (Swift LLM processing/execution engine), agent (macOS work-queue AI worker loop), and mind (agentic processing) all need a model endpoint; mlx-router can serve them an on-device OpenAI-compatible backend instead of a paid cloud API. laniakea (LAN AI scripts → local bin) shares the same "keep AI on local/LAN hardware" philosophy and is a natural front-end for distributing access to a mlx-router instance across a network. saixha and yobro, as AI-driven shells/assistants, are likewise potential clients. Build/spec tooling such as ybs, dagsmith, and murphy can orchestrate workloads that call into it, and memory provides the persistence layer those agents pair with the inference mlx-router supplies.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

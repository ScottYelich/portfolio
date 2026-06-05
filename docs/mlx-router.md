# mlx-router — executive summary

**One-liner:** A single OpenAI-compatible endpoint for Apple Silicon that intelligently routes each request to the right-sized local MLX model — fast 7B for chat, Coder-32B for code, 72B for hard reasoning — with tool calling, KV-cache-aware session affinity, and a self-managing process daemon behind it.

## What it provides
- **One smart entry point** (`:7777`) speaking the OpenAI Chat Completions API (`/v1/chat/completions`, `/v1/models`), so Aider, the OpenAI SDK, and curl clients work unchanged against fully local inference.
- **Tiered routing** across 72B / 32B / 14B / 7B model tiers (Qwen2.5 family) plus a 0.5B router-classifier tier. Requests are dispatched, in priority order, by `X-Force-Model` header, prefix alias (`:1`/`:2`/`:3`, `math:`, `code:`, `deep:`, `fast:`, etc., configurable), per-conversation affinity, keyword match, ~160ms LLM classification, or default tier.
- **Session affinity for KV-cache reuse:** hashes the first user message so multi-turn conversations stay pinned to the same backend, cutting latency on follow-ups.
- **Tool calling** via prompt injection (native mlx_textgen tool support is unreliable on Qwen), with multi-format detection (XML tags, raw/newline-delimited JSON, truncated-JSON fallback) converted back to proper OpenAI streaming `tool_calls`; tools are auto-stripped for 7B to avoid crashes.
- **In-chat commands** (`:+`/`:-` tier tags, `:=` stats, `:?` help) and routing-metadata response headers (`X-Routed-To`, `X-Route-Method`, `X-Route-Time-Ms`, `X-Backend-Port`, `X-Queue-Position`).
- **Process management:** an `mlx` CLI and Unix-socket daemon that start/stop/swap/restart model servers with pre-load RAM checks, warmup inference, auto-restart with backoff, request timeouts, queue backpressure (HTTP 429), benchmarking (`tok/s`, TTFT, stress mode), and orphan-process adoption.

## Strengths
- Right-sizes compute per request: cheap models handle easy traffic while big models are reserved for hard work, improving throughput and latency without client changes.
- Drop-in OpenAI compatibility — slots under existing tooling with zero code changes and no API key required.
- Fully local and private: all inference and data stay on-device, no outbound calls, good for sensitive or offline use.
- Operationally serious for a local stack: RAM gating, warmup, auto-restart, backpressure, configurable timeouts, and benchmarking are built in rather than bolted on.
- Tuned for Apple Silicon via MLX + mlx_textgen, with KV-cache persistence and affinity to exploit it.

## Weaknesses / limitations
- Apple-Silicon-and-macOS-14+-only — no Intel, Linux, or non-Mac path.
- Hardware-hungry: the full multi-tier setup targets large-RAM machines (e.g. M3 Ultra 256GB); a 72B tier alone needs ~45GB and the documented default layout runs many 32B instances.
- No authentication, rate limiting, or TLS — safe only on a trusted local/LAN boundary; defaults bind locally.
- Tool calling relies on prompt injection and heuristic output parsing rather than native function-calling, so reliability depends on model behavior and the fallback parsers.
- Qwen-centric: model tiers and routing keywords assume the Qwen2.5 family; other models would need reconfiguration.
- Some bundled docs lag the code (e.g. mlx-manager.md still says the daemon does not auto-restart, while the router CLI now supports auto-restart/`restart`/`restart-all`).

## Why you'd use it
Reach for mlx-router when you want one private, cost-free, OpenAI-compatible endpoint on a Mac that automatically picks the cheapest model that can do the job — for local development, coding agents, offline experimentation, or privacy-sensitive prompts. Choose it over a hosted API when data locality, zero marginal cost, and Apple Silicon performance matter more than scale or multi-tenancy, and over a single-model local server when you want tiered cost/latency trade-offs, tool use, and process supervision without wiring them yourself.

## How it relates to the other projects
mlx-router is the local inference backend the rest of the portfolio calls. murphy (LLM engine), agent (work-queue daemon), saixha (S-expr shell), and yobro (local voice assistant) all need a model endpoint and can point their OpenAI-compatible client at mlx-router instead of a paid cloud API. laniakea (the LAN AI stack) shares the keep-AI-on-local/LAN-hardware philosophy and is a natural way to distribute access to a mlx-router instance across a network. Supporting tools (gws, gmail-utility, and similar) can likewise route their LLM calls here. Within this portfolio, mlx-router is the inference substrate; the other projects are its clients and orchestrators.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

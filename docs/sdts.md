# sdts — executive summary

**One-liner:** A full-stack algorithmic-trading lab where a hand-rolled secure UDP networking framework, a zero-config service mesh, and a real-time terminal dashboard let trading bots discover each other, place bracket orders, and stream ticks across machines.

## What it provides
SDTS (Scott & Daniel Trading System) bundles three production-ready layers in one repo. The **YX Framework** is a dual-language (Python + Swift, fully interoperable) secure UDP/P2P networking stack with a 5-layer design, JSON-RPC and binary/chunked protocols, HMAC-SHA256 validation, AES-256-GCM encryption, compression, and replay protection. **AlgoTrader** is a broadcast-based distributed service mesh built on YX that handles zero-config peer discovery (heartbeats), lifecycle management (spawn/restart/auto-restart policies), metrics, logs, and a 9-view ASCII dashboard plus a 10Hz live-trading CLI. The **MES Trading System** adds state-machine futures simulators and Interactive Brokers (TWS/Gateway) data fetchers for Micro E-mini S&P 500 contracts, with momentum signals and bracket orders.

## Strengths
- Genuinely complete and tested: dual Python/Swift YX with 20/20 interoperability tests and 94+ Swift unit tests; AlgoTrader's trading-utils carry 200+ tests.
- Strong operational discipline baked into docs: locked Architecture Decision Records (ADRs), proof-based "no claims without evidence" rules, and an anti-thrashing challenge protocol.
- Zero-configuration networking — services find each other via UDP broadcast heartbeats with no hard code dependencies, so workspaces interoperate cleanly.
- Cross-platform service management (macOS launchd, Linux systemd, WSL2) with real-time observability built in.
- Real broker integration (IBKR paper/live) plus simulators, so the same mesh spans backtesting and live execution.

## Weaknesses / limitations
- Custom-rolled crypto/networking (HMAC + AES-GCM over raw UDP) is ambitious to maintain and audit versus using a vetted transport (TLS/QUIC/mTLS); security depends on shared keys.
- Broadcast-only architecture (255.255.255.255, SO_REUSEPORT) is a deliberate constraint that limits the topology to a single LAN segment and adds noise at scale.
- Version drift in the docs: README claims YX v2.0.0 while CLAUDE.md references v1.0.3, indicating the documentation set has not fully converged.
- Heavy reliance on per-developer workspaces (scott/, daniel/) means much logic lives outside shared infrastructure and isn't uniformly hardened.
- Private/personal project (no open license, single primary author per component), small contributor base, and trading-specific scope; this is research/lab tooling, not turnkey production trading software.

## Why you'd use it
Reach for SDTS when you want a self-contained sandbox for distributed algorithmic trading: a place to run multiple trading services across LAN machines, watch ticks and orders live in a terminal, and wire signal generators to a broker — without standing up heavyweight infrastructure. It's most valuable as a learning/experimentation platform and as a reference for how to build a secure, discoverable service mesh from primitives.

## How it relates to the other projects
SDTS shares DNA with **yx** (the yx packet / data-protocol project) — the YX networking framework here is the same lineage of UDP packet format and secure transport. Its broadcast-discovery, daemon-driven service mesh echoes the operational pattern of **agent** (the macOS work-queue daemon / AI worker loop in Swift) and **murphy** (Swift execution engine), all favoring autonomous, long-running processes that coordinate over messages rather than tight coupling. The proof-based, ADR-governed engineering rigor mirrors the disciplined, spec-first ethos seen across the portfolio's build-methodology tooling (**ybs**, **dagsmith**). Within the broader portfolio it is the domain-specific trading vertical, standing apart from the AI/LLM-centric repos while sharing their distributed-systems and Swift/Python craftsmanship.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

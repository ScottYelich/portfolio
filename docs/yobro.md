# yobro — executive summary

**One-liner:** A 100% local, always-on "Alexa clone" for macOS that wakes to "yo bro," answers in a 229B-parameter local LLM's words, and can speak back in a clone of your own voice — no cloud, no API keys.

## What it provides
- An always-listening voice pipeline: mic capture → CPU voice-activity detection → local speech-to-text → wake-word check → local LLM → text-to-speech → audio playback, looping continuously.
- Wake words/phrases ("yo bro," "hey bro," "yo geek," "hey dad") recognized via a lightweight VAD+STT loop rather than a dedicated wake-word model, so no extra model to download or train.
- Two TTS modes: a fast preset voice (Kokoro-82M, sub-200ms) and a zero-shot voice clone (F5-TTS) of the user from a ~15-20s reference recording, set up interactively via `yobro setup-voice`.
- A small, installable Python CLI (`yobro listen`, `yobro setup-voice`) that orchestrates external local services rather than bundling models itself.

## Strengths
- Fully local and private: all inference runs on-device (M3/M4-class Apple Silicon), with no cloud calls, accounts, or credentials.
- Reuses existing local infrastructure (voice-server STT/TTS on :7022, mlx-router LLM on :7777) instead of reinventing it — the daemon is thin and focused.
- Clever wake-word approach: piggybacks on already-running STT, avoiding a separate wake-word model while keeping trigger words editable in one Python dict.
- Personalization: speaks back in the user's own cloned voice with a one-time setup.
- Cleanly built and documented via the YBS 2.0 spec/step methodology (features, technical-specs, ADRs, acceptance-tests, build steps all present).

## Weaknesses / limitations
- Heavy external dependency footprint: needs voice-server, mlx-router, and (for cloning) f5-tts-clone all running on a specific high-end Mac before it functions — not self-contained or plug-and-play.
- Tightly coupled to one home setup, including a hardcoded LAN host for the LLM, so portability to other machines/networks requires reconfiguration.
- The VAD+STT wake-word strategy adds ~300-500ms latency and is less robust than a purpose-built wake-word detector; voice-clone TTS adds 2-5s per response.
- macOS-only (relies on `afplay`); no cross-platform support.
- No README; documentation lives in CLAUDE.md and docs/. Async intent-routing / agent-job-queue integration is still on the roadmap (deferred), so today it answers conversationally but does not yet dispatch background tasks like sending email.

## Why you'd use it
Use yobro when you want a private, hands-free voice assistant on your own Mac that never touches the cloud — for casual Q&A, quick spoken answers, and experimenting with local STT/LLM/TTS and personal voice cloning. It is best suited to someone already running a local MLX-based AI stack who values privacy and customization over turnkey convenience.

## How it relates to the other projects
yobro is built with **ybs** (the S-expression spec/step build methodology — its `specs/`, `steps/`, and `step-plans/` are all `.ybs` graphs). It is the voice front-end of a broader local-AI ecosystem: it routes LLM queries through **mlx-router** (local MLX inference) and can hand off to **murphy** (the Swift LLM execution engine), which can in turn call yobro for spoken responses. Its thin deploy wrapper lives alongside **laniakea** (LAN AI scripts → local bin). The deferred roadmap connects it to **agent** (the macOS work-queue daemon) for async intent routing and to **gws**/**gmail-utility** for calendar/email actions spoken aloud. It is one repo in the [ScottYelich portfolio](https://scottyelich.github.io/portfolio/).

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

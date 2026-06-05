# gws — executive summary

**One-liner:** A fast, JSON-only command-line wrapper around the Gmail and Google Sheets APIs, built to be driven by AI agents and shell scripts instead of a browser.

## What it provides
- A single `gws` CLI exposing real-time Gmail operations (search, read message, read thread, create drafts, list labels) and Google Sheets operations (read, write, append, batch-update, create spreadsheet).
- Every command emits valid JSON to stdout and JSON errors to stderr, so an LLM tool caller can `json.loads(stdout)` unconditionally — no browser automation, no MCP server, no persistent process.
- One-time OAuth2 setup via InstalledAppFlow, then fully headless silent token refresh; sub-second API round-trips (~200–500ms per invocation including Python startup).
- A complete YBS 2.0.0 specification graph (features, functional/technical requirements, ADRs, acceptance tests, security threats) plus executable build steps, so the implementation can be regenerated from spec by an AI executor.

## Strengths
- Purpose-built for subprocess/agent invocation: uniform JSON contract makes it trivial for Murphy, Claude, or any script to call and parse.
- Much faster and more reliable than screen-scraping or browser-driving a spreadsheet UI.
- Small, focused dependency surface (google-api-python-client, google-auth, Click) and a clean service-class layout (auth/gmail/sheets) that is also importable.
- Fully spec-driven via YBS: the repo documents its own requirements, decisions, and tests, and BUILD_STATUS shows a clean end-to-end build from steps 0–6.
- Security-conscious by design: credentials/token excluded from git, token written `0600`, explicit revocation guidance.

## Weaknesses / limitations
- Narrow surface area: only Gmail and Sheets are implemented despite "Workspace" framing — no Calendar, Drive, or Docs commands yet (Drive/Calendar scopes are requested but unused).
- Gmail is read-plus-draft only; it cannot send mail, modify labels on messages, or delete — write capability is deliberately limited.
- Single-user, desktop OAuth model (InstalledAppFlow, not service accounts), so it does not fit server/multi-tenant or domain-wide automation.
- Per-call Python process startup adds latency and makes it unsuitable for high-throughput batch loops where a long-lived service would be better.
- Spec metadata still marks the three features as "draft," and there is no visible automated test execution evidence beyond the YBS acceptance-test specs.

## Why you'd use it
Reach for `gws` when an AI agent or shell script needs to programmatically search live Gmail or read/write Google Sheets in a tool-call loop and wants guaranteed parseable JSON output with minimal latency. It is the right tool for real-time Workspace read/write from automation — not for bulk archiving, not for human interactive use, and not for server-side multi-account deployments.

## How it relates to the other projects
gws is built with **ybs** (the spec/step methodology and S-expression `.ybs` graph format), and its specs/steps directories are the concrete output of that methodology. It is explicitly designed as a callable tool for **murphy** (the Swift LLM execution engine) and for the broader agentic stack — **agent** (work-queue daemon/AI worker loop), **mind** (agentic processing), and **saixha** (S-expression AI shell) — any of which can shell out to `gws` to act on Gmail or Sheets and consume its JSON. It is a deliberate sibling to **gmail-utility**: gmail-utility does local archiving (SQLite + .eml) for offline search, while gws does real-time API read/write; they share the OAuth2 pattern but zero code and use separate token files. Like **yobro**, it demonstrates the ybs-built application pattern within the portfolio.

---
*Executive summary — condensed from this repo's own docs. Part of [ScottYelich · portfolio](https://scottyelich.github.io/portfolio/), the public starting point for these projects.*

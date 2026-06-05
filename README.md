# ScottYelich · portfolio

An interactive, public, **self-contained** index of my repositories — public and private.
Private repos are listed for context (name, description, tags); their links require access.

**Live page:** https://scottyelich.github.io/portfolio/

## What's here
- `index.html` — the page. CSS and repo data are **embedded** (no external fetch); works on
  GitHub Pages and via `file://`.
- `style/portfolio.css` — canonical source of the shared style; inlined into `index.html`
  with a provenance header (version, date, sha256).
- `vendor/echarts.min.js` — vendored Apache ECharts **6.0.0** (offline, pinned).
- `build.sh` — regenerates the embedded blocks from your GitHub account via `gh`.
- `CLAUDE.md` / `NOTES.md` — conventions and the reasoning behind them.

## Update the list
```bash
./build.sh            # defaults to ScottYelich
./build.sh someuser   # any GitHub user
```
Requires an authenticated [`gh`](https://cli.github.com/), `python3`, and `shasum`.

## How it works
- **Data** is one embedded S-expression (`(portfolio (repo …) …)`) parsed by a tiny in-page
  reader — code = data, no JSON fetch.
- **Style** is inlined from `style/portfolio.css`; the embedded copy is versioned, dated, and
  integrity-hashed so it can be checked against the source for updates.
- **Charts** use the locally-vendored ECharts (no CDN).

See [NOTES.md](NOTES.md) for the conventions (placeholder syntax, embedding/provenance, etc.).

## View locally
Open `index.html` in a browser — no build step, no server.

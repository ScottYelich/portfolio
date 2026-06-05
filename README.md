# ScottYelich · portfolio

An interactive, public index of my repositories — public and private. Private repos are
listed for context (name, description, tags); their links require access.

**Live page:** https://scottyelich.github.io/portfolio/

## What's here
- `index.html` — interactive directory: search, filter by public/private, click tags to filter.
- `data.js` — the repo metadata (`window.REPOS`), loaded as a plain script so the page works
  both on GitHub Pages **and** when opened locally (`file://`) — no server needed.
- `build.sh` — regenerates `data.js` from your GitHub account via `gh`.

## Update the list
```bash
./build.sh            # defaults to ScottYelich
./build.sh someuser   # any GitHub user
```
Requires an authenticated [`gh`](https://cli.github.com/) and `python3`. Tags are auto-derived
from language, GitHub topics, and keyword categories (see `CATEGORIES` in `build.sh`); edit
`data.js` by hand afterward if you want — just remember a re-run of `build.sh` overwrites it.

## View locally
Just open `index.html` in a browser — no build step, no server.

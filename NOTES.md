# NOTES — conventions & rationale

The "why" behind the conventions in [CLAUDE.md](CLAUDE.md).

## Path placeholders: why `{{name}}`

Goal: references to "where a repo is cloned" must contain **no hardcoded paths and no
assumed locations**. Each repo is independently located and truly unknown until linked
later. Candidates considered:

| Form | Concise | Collides w/ host syntax | Hyphen-safe (`mlx-router`) | Silent-empty if unbound | Notes |
|------|:--:|:--:|:--:|:--:|------|
| `${name}` | ✅ | ❌ shell `${}` + JS template literals | ❌ `bad substitution` | ❌ expands to empty → wrong path | `${n:-/tmp}` default is shell-only + a footgun |
| `@name@` | ✅ | ✅ none | ✅ | ✅ fails loud | autoconf-style; ad-hoc, no default |
| `((name))` | ✅ | ❌ **valid Scheme** (nested call); `(let ((x …)))` everywhere | ✅ | n/a | **worst** in an S-expr codebase — a reader evaluates it |
| `{{name}}` | ✅ | ✅ none (foreign to md/py/swift/js/scheme) | ✅ | ✅ fails loud | matches YBS's own `{{…}}` family |

**Decision: `{{name}}`.** A placeholder sentinel must be *foreign* to every language it
sits in. Parens are the *native* syntax of our S-expression files (ybs, saixha) — exactly
the thing to avoid. `{{…}}` is foreign everywhere, greps cleanly (`\{\{[a-z0-9_-]+\}\}`),
is hyphen-safe, and never silently expands.

A bare `{{ybs}}` is distinct from YBS build-config markers, which match `{{CONFIG:…}}`.
When a value genuinely has a safe default, use the full YBS marker
`{{CONFIG:key|type|description|default}}` — that gives a forced-config substitution model
*with* a default (the safety the `${n:-/tmp}` idea was reaching for), done portably.

### Why not just env vars (`${ybs}`)?
- Only shell honors `${}`/`:-`. In `.md`, `.py`, `.swift`, `.js` it's inert literal text,
  so the "live var" idea covers only a fraction of references.
- Hyphenated repo names (`mlx-router`, `gmail-utility`) aren't valid shell identifiers.
- Unset → empty → `cd ${gws} && …` silently runs in the wrong directory. Better to fail loud.

## S-expressions: two different jobs, don't conflate
- **Placeholders** → want a *foreign, inert* sentinel → `{{name}}` (parens forbidden).
- **Portfolio data** → genuinely *is* an S-expression read by a reader → real `(...)` is
  correct and on-theme ("code = data = pipe format").

## Embedding + provenance
Shared assets are inlined (never linked) for self-containment, but each embedded copy
records `source` + `version` + `date` + `sha256` so it stays verifiable and update-checkable
against the canonical source in this repo.

- **Integrity / "signed":** sha256 of the source file today. To upgrade to a real digital
  signature, sign the source and add a `signature:`/`minisign:`/`cosign:` line to the
  provenance header (e.g. `minisign -Sm style/portfolio.css`), then verify against a
  published public key. The header format already has room for it.
- **Versioned:** `@version` in the source; bump on change.
- **Dated:** UTC build time stamped at embed.

## ECharts
Vendored at `vendor/echarts.min.js`, pinned to **6.0.0** (latest is 6.1.0; pinned on
purpose). Provenance in `vendor/echarts.provenance.txt` (source URL, version, sha256, fetch
date). Self-hosted rather than CDN so the page works offline and can't drift.

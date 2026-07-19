# CLAUDE.md — portfolio

**Version**: 0.1.0
**Last Updated**: 2026-06-05

Guidance for AI agents (and humans) working in this repo.

## What this is

A **public, self-contained, interactive index** of my repositories — public and private.
Private repos are listed for context (name, description, tags); their links require access.
Served via GitHub Pages at https://scottyelich.github.io/portfolio/ and clonable.

## Files

| File | Role |
|------|------|
| `index.html` | The page. **Fully self-contained**: CSS, data, **and ECharts** are all embedded. One file, draggable anywhere. |
| `style/portfolio.css` | **Canonical source** of the shared style. Embedded into `index.html`; never `<link>`ed. |
| `vendor/echarts.min.js` | **Canonical source** of Apache ECharts **6.0.0** (offline, version-pinned). Embedded into `index.html`, never `<script src>`ed. See `vendor/echarts.provenance.txt`. |
| `build.sh` | Regenerates the embedded blocks from live `gh` data + `style/portfolio.css`. |
| `NOTES.md` | Rationale for the conventions below (the "why"). |

Rebuild: `./build.sh` (requires `gh`, `python3`, `shasum`). Opens directly via `file://` too — no server.

## Conventions

### 1. Always embed; reference the source for update-checks
Shared/vendored assets (CSS and ECharts) are **inlined**, never linked. Each embedded copy
carries a **provenance header** so a consumer can verify integrity and check for updates:

```
/*! EMBEDDED ASSET — portfolio.css
 * source:  https://github.com/ScottYelich/portfolio/blob/main/style/portfolio.css
 * version: 0.1.0          <- bump @version in the source on any change
 * date:    <UTC build time>
 * sha256:  <hash of the source file>   <- integrity ("signed")
 */
```

`portfolio` is the **source of truth**: edit `style/portfolio.css`, bump its `@version`,
re-run `build.sh`. The embedded header records where it came from and which version/hash,
so downstream copies stay **versioned, dated, integrity-hashed**. (A real cryptographic
signature can replace/augment the sha256 later — see NOTES.)

### 2. Data is an embedded S-expression (code = data)
Repo data lives **inside** `index.html` as one S-expression, parsed by a ~30-line reader:

```scheme
(portfolio
  (generated "2026-06-05T…Z")
  (repo (name "ybs") (visibility private) (description "…")
        (url "…") (homepage "") (language "Shell") (updated "…")
        (tags "devtools" "Shell"))
  …)
```

Real parens are **correct here** — this genuinely *is* an S-expression, read by a reader.
That is different from path placeholders (next), where parens would be wrong.

### 3. Path references use `{{name}}` placeholders — never hardcoded paths
No repo's location is assumed. Cross-references to where something is cloned use a
**brace placeholder**, unbound until linked later:

```
${ybs}/framework   ->   WRONG (shell-expands to empty; breaks on hyphens)
@ybs@              ->   ok but ad-hoc
((ybs))            ->   WRONG: valid Scheme (nested call); collides with (let ((x …)))
{{ybs}}            ->   ✅ foreign to md/py/swift/js AND scheme; greppable; hyphen-safe
```

Rules: never write `/Users/...`, `~/workspace/...`, or any absolute/assumed path. Use
`{{<repo-name>}}` (e.g. `{{mlx-router}}`). A value with a sane default may use YBS's own
`{{CONFIG:key|type|desc|default}}` marker. See NOTES.md for the full reasoning.

## Version History
- **0.1.0** (2026-06-05): Initial — embedded S-expression data, inlined CSS w/ provenance, vendored ECharts 6.0.0.

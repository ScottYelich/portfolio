#!/usr/bin/env bash
# Rebuild the embedded blocks of index.html from live GitHub data + style/portfolio.css.
#   - Repo data  -> embedded S-expression between ;; DATA:START / ;; DATA:END
#   - Stylesheet -> inlined from style/portfolio.css with a provenance header
#                   (source + version + date + sha256) between /* CSS:START */ / /* CSS:END */
# Usage: ./build.sh [github-user]   (default: ScottYelich).  Requires: gh, python3, shasum.
set -euo pipefail
USER="${1:-ScottYelich}"
cd "$(dirname "$0")"

echo "Fetching repos for $USER ..."
gh repo list "$USER" --limit 500 \
  --json name,description,visibility,url,homepageUrl,primaryLanguage,repositoryTopics,pushedAt,isArchived,isFork,diskUsage \
  > /tmp/portfolio_repos.json

GEN="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
CSS_VERSION="$(grep -m1 '@version' style/portfolio.css | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')"
CSS_SHA="$(shasum -a 256 style/portfolio.css | awk '{print $1}')"

python3 - "$GEN" "$CSS_VERSION" "$CSS_SHA" <<'PY'
import json, sys, re

import os
gen, css_ver, css_sha = sys.argv[1], sys.argv[2], sys.argv[3]
repos = json.load(open("/tmp/portfolio_repos.json"))
try:
    taglines = json.load(open("data/taglines.json"))
except Exception:
    taglines = {}
try:
    scores = {k: v for k, v in json.load(open("data/scores.json")).items() if not k.startswith("_")}
except Exception:
    scores = {}

def esc(s):  # escape for an S-expression string literal
    return (s or "").replace("\\", "\\\\").replace('"', '\\"')

CATS = {
    "trading":  r"trad|market|stock|algo|sdts",
    "ai":       r"\bai\b|llm|agent|mlx|mind|memory|chat|alexa|shell|sasha|saixha|murphy|laniakea|yobro",
    "google":   r"google|gmail|workspace|\bgws\b",
    "devtools": r"build|orchestrat|\bdag\b|ybs|router|proxy|smith",
}
def tags_for(r, lang):
    out, seen = [], set()
    blob = f"{r['name']} {r.get('description') or ''}".lower()
    cand = [c for c, p in CATS.items() if re.search(p, blob)]
    cand += [(t or {}).get("name") for t in (r.get("repositoryTopics") or []) if (t or {}).get("name")]
    if lang: cand.append(lang)
    if r.get("isArchived"): cand.append("archived")
    for t in cand:
        if t and t.lower() not in seen:
            seen.add(t.lower()); out.append(t)
    return out

lines = ["(portfolio", f'  (generated "{gen}")']
for r in sorted(repos, key=lambda x: x.get("pushedAt") or "", reverse=True):
    lang = (r.get("primaryLanguage") or {}).get("name") or ""
    vis  = (r.get("visibility") or "").lower()
    tags = " ".join(f'"{esc(t)}"' for t in tags_for(r, lang))
    name = r["name"]
    summary = taglines.get(name, "")
    doc = f"docs/{name}.html" if os.path.exists(f"docs/{name}.html") else ""
    sc = scores.get(name, {})
    lines += [
        "  (repo",
        f'    (name "{esc(name)}")',
        f'    (visibility {vis})',
        f'    (description "{esc(r.get("description") or "")}")',
        f'    (summary "{esc(summary)}")',
        f'    (doc "{esc(doc)}")',
        f'    (url "{esc(r["url"])}")',
        f'    (homepage "{esc(r.get("homepageUrl") or "")}")',
        f'    (language "{esc(lang)}")',
        f'    (updated "{(r.get("pushedAt") or "")[:10]}")',
        f'    (size {r.get("diskUsage", 0)})',
        f'    (complexity {sc.get("complexity", 0)})',
        f'    (maturity {sc.get("maturity", 0)})',
        f'    (tags {tags}))',
    ]
lines.append(")")
sexp = "\n".join(lines)

prov = (
    "/*! EMBEDDED ASSET — portfolio.css\n"
    " * source:  https://github.com/ScottYelich/portfolio/blob/main/style/portfolio.css\n"
    f" * version: {css_ver}\n"
    f" * date:    {gen}\n"
    f" * sha256:  {css_sha}\n"
    " * note:    inlined for self-containment; check source for updates.\n"
    " */\n"
)
css = open("style/portfolio.css").read()

html = open("index.html").read()
html = re.sub(r"(;; DATA:START).*?(;; DATA:END)",
              lambda m: m.group(1) + "\n" + sexp + "\n" + m.group(2), html, flags=re.S)
html = re.sub(r"(/\* CSS:START \*/).*?(/\* CSS:END \*/)",
              lambda m: m.group(1) + "\n" + prov + css + m.group(2), html, flags=re.S)
open("index.html", "w").write(html)

pub = sum(1 for r in repos if (r.get("visibility") or "").lower() == "public")
print(f"Embedded {len(repos)} repos ({pub} public) as S-expression.")
print(f"Inlined portfolio.css v{css_ver}  sha256={css_sha[:16]}…")
PY

echo "Done. index.html is self-contained (open it directly or via Pages)."

#!/usr/bin/env python3
"""Versioned, dated REPORT TEMPLATE — one interactive report per repo.

v1.1.0 layout: capability RADAR (left, 8 axes, vs portfolio average) + anatomy
SUNBURST (right, real file composition), then the rendered executive summary.

Scores come from data/scores.json (single source of truth, also used by the index
complexity×maturity chart). Composition is computed from `git ls-files` (real).

Run from the portfolio repo root:  python3 tools/build-reports.py
Requires: gh (auth), pandoc, git, vendor/echarts.min.js.
"""
import json, subprocess, os, html, datetime, collections, hashlib, re

TEMPLATE_VERSION = "1.1.0"
PORTFOLIO_URL = "https://scottyelich.github.io/portfolio/"

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
os.chdir(root)
date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout

css = open("style/readme.css", encoding="utf-8").read()
report_css = open("style/report.css", encoding="utf-8").read()

# ECharts is EMBEDDED (never <script src>) so every report is 100% self-contained.
echarts_src = open("vendor/echarts.min.js", encoding="utf-8").read()
echarts_sha = hashlib.sha256(open("vendor/echarts.min.js", "rb").read()).hexdigest()
_prov = open("vendor/echarts.provenance.txt", encoding="utf-8").read()
_m = re.search(r"^version:\s*([0-9.]+)", _prov, re.M)
ECHARTS_VERSION = _m.group(1) if _m else "6.0.0"
ECHARTS_EMBED = (
    "<!-- Vendored, version-pinned & EMBEDDED. See vendor/echarts.provenance.txt -->\n"
    "<script>\n"
    "/*! EMBEDDED ASSET — echarts.min.js\n"
    f" * source:  https://cdn.jsdelivr.net/npm/echarts@{ECHARTS_VERSION}/dist/echarts.min.js\n"
    f" * library: Apache ECharts {ECHARTS_VERSION} (Apache-2.0)\n"
    f" * date:    {date}\n"
    f" * sha256:  {echarts_sha}\n"
    " * note:    inlined for self-containment; see vendor/echarts.provenance.txt.\n"
    " */\n" + echarts_src + "\n</script>"
)
taglines = json.load(open("data/taglines.json", encoding="utf-8"))
scores = json.load(open("data/scores.json", encoding="utf-8"))
scores = {k: v for k, v in scores.items() if not k.startswith("_")}

meta = json.loads(sh("gh", "repo", "list", "ScottYelich", "--limit", "500",
                     "--json", "name,visibility,primaryLanguage,url,diskUsage") or "[]")
metaby = {m["name"]: m for m in meta}

RADAR = [("Value","value"),("Maturity","maturity"),("Complexity","complexity"),
         ("Reusability","reusability"),("Autonomy","autonomy"),("Docs","docs"),
         ("Tests","tests"),("LLM-reliance","llm")]
avg = {k: round(sum(scores[r][k] for r in scores) / len(scores)) for _, k in RADAR}

CAT = {}
for e in "swift py js ts tsx jsx go rs c h cc cpp hpp m mm rb java kt lua sh bash zsh pl".split(): CAT[e]="Code"
for e in "md markdown txt rst adoc".split(): CAT[e]="Docs"
for e in ["ybs"]: CAT[e]="Specs"
for e in "json yaml yml toml ini cfg conf lock env".split(): CAT[e]="Config"
for e in "html css scss".split(): CAT[e]="Web"
for e in "csv tsv sql".split(): CAT[e]="Data"

def composition(repo):
    cats = {}
    for line in sh("git", "-C", f"../{repo}", "ls-files").splitlines():
        base = line.strip().rsplit("/", 1)[-1]
        if not base: continue
        ext = base.rsplit(".", 1)[-1].lower() if "." in base else base.lower()
        cat = CAT.get(ext, "Other")
        cats.setdefault(cat, collections.Counter())[ext] += 1
    data = []
    for cat, exts in sorted(cats.items(), key=lambda kv: -sum(kv[1].values())):
        top = exts.most_common(7)
        children = [{"name": ("." + e if e.isalnum() else e), "value": n} for e, n in top]
        data.append({"name": cat, "children": children})
    return data

CHART_JS = r"""
function R(id,o){var c=echarts.init(document.getElementById(id),null,{renderer:'canvas'});
 o.backgroundColor='transparent';c.setOption(o);addEventListener('resize',function(){c.resize();});return c;}
var C=['#58a6ff','#3fb950','#d29922','#bc8cff','#f778ba','#39c5cf','#ff7b72','#a5d6ff'];
if(window.echarts){
 R('radar',{tooltip:{},legend:{data:[SUBJECT,'portfolio avg'],textStyle:{color:'#8b949e'},top:0},
  radar:{indicator:AXES.map(function(n){return {name:n,max:100};}),splitNumber:4,
   splitLine:{lineStyle:{color:'#21262d'}},splitArea:{areaStyle:{color:['rgba(88,166,255,.03)','rgba(88,166,255,.06)']}},
   axisName:{color:'#8b949e',fontSize:11}},
  series:[{type:'radar',data:[
   {value:RVAL,name:SUBJECT,areaStyle:{color:'rgba(88,166,255,.25)'},lineStyle:{color:C[0],width:2},itemStyle:{color:C[0]}},
   {value:AVG,name:'portfolio avg',areaStyle:{color:'rgba(139,148,158,.10)'},lineStyle:{color:'#8b949e'},itemStyle:{color:'#8b949e'}}]}]});
 if(SUN.length){
  R('sun',{tooltip:{formatter:function(p){return p.name+': '+p.value;}},
   series:[{type:'sunburst',data:SUN,radius:[0,'95%'],sort:null,
    label:{color:'#0d1117',fontSize:10,minAngle:8},itemStyle:{borderColor:'#0d1117',borderWidth:2},
    levels:[{},{r0:0,r:'46%',label:{rotate:0}},{r0:'46%',r:'95%'}],color:C}]});
 } else { document.getElementById('sun').parentNode.style.display='none'; }
} else { var rc=document.querySelector('.report-charts'); if(rc) rc.style.display='none'; }
"""

count = 0
for name, tag in taglines.items():
    md = f"docs/{name}.md"
    if not os.path.exists(md): continue
    m = metaby.get(name, {})
    vis = (m.get("visibility") or "").lower()
    lang = (m.get("primaryLanguage") or {}).get("name") or "—"
    size = m.get("diskUsage", 0)
    url = m.get("url") or f"https://github.com/ScottYelich/{name}"
    site = f"https://scottyelich.github.io/{name}/"
    s = scores.get(name, {k: 0 for _, k in RADAR})
    rval = [s.get(k, 0) for _, k in RADAR]
    aval = [avg[k] for _, k in RADAR]
    sun = composition(name)
    nfiles = sum(sum(c["value"] for c in cat["children"]) for cat in sun)
    body = sh("pandoc", md, "-f", "gfm", "-t", "html5")
    badge = f'<span class="badge {vis}">{vis}</span>' if vis else ""
    stats = " · ".join(filter(None, [html.escape(lang), f"{nfiles} files",
                                     f"{size} KB", f"report template v{TEMPLATE_VERSION}"]))
    data_js = ("const SUBJECT=" + json.dumps(name) + ";const AXES=" + json.dumps([a for a, _ in RADAR]) +
               ";const RVAL=" + json.dumps(rval) + ";const AVG=" + json.dumps(aval) +
               ";const SUN=" + json.dumps(sun) + ";")
    head = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="report-template-version" content="{TEMPLATE_VERSION}">
<title>{html.escape(name)} · report</title>
<style>
{css}{report_css}</style>
</head>
<body>
<div class="wrap">
  <nav class="topbar">
    <a class="home" href="{PORTFOLIO_URL}">← Portfolio</a>
    <span class="crumb">{html.escape(name)} · report</span>
    <a class="src" href="{html.escape(url)}" target="_blank" rel="noopener">repo ↗</a>
    <a href="{html.escape(site)}" target="_blank" rel="noopener">site ↗</a>
  </nav>
  <header class="rep-head">
    <h1>{html.escape(name)} {badge}</h1>
    <p class="rep-tag">{html.escape(tag)}</p>
    <p class="rep-stats">{stats}</p>
  </header>
  <div class="report-charts">
    <div class="rc"><h3>Capability radar <span class="q">vs portfolio average</span></h3><div class="c" id="radar"></div></div>
    <div class="rc"><h3>Anatomy &amp; composition <span class="q">real file make-up</span></h3><div class="c" id="sun"></div></div>
  </div>
  <article class="markdown-body">
{body}
  </article>
  <footer class="foot">Report template v{TEMPLATE_VERSION} · generated {date} · <a href="{PORTFOLIO_URL}">ScottYelich · portfolio</a></footer>
</div>
{ECHARTS_EMBED}
<script>{data_js}</script>
<script>{CHART_JS}</script>
</body>
</html>
"""
    open(f"docs/{name}.html", "w", encoding="utf-8").write(head)
    count += 1
    print(f"  report: docs/{name}.html  ({nfiles} files, radar+sunburst)")

print(f"Generated {count} reports — template v{TEMPLATE_VERSION} @ {date}")

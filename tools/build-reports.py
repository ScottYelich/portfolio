#!/usr/bin/env python3
"""Versioned, dated REPORT TEMPLATE — generates one interactive report per repo.

Each docs/<repo>.html report = stats strip + an embedded ECharts commit-activity chart
+ the rendered executive summary. Uniform format across every repo. Bump TEMPLATE_VERSION
when the format changes, then re-run to update every report.

Run from the portfolio repo root:  python3 tools/build-reports.py
Requires: gh (auth), pandoc, git, the vendored vendor/echarts.min.js.
"""
import json, subprocess, os, html, datetime, collections

TEMPLATE_VERSION = "1.0.0"
PORTFOLIO_URL = "https://scottyelich.github.io/portfolio/"

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(here)
os.chdir(root)
date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

css = open("style/readme.css", encoding="utf-8").read()
report_css = open("style/report.css", encoding="utf-8").read()
taglines = json.load(open("data/taglines.json", encoding="utf-8"))

meta = json.loads(subprocess.run(
    ["gh", "repo", "list", "ScottYelich", "--limit", "500",
     "--json", "name,visibility,primaryLanguage,url"],
    capture_output=True, text=True).stdout or "[]")
metaby = {m["name"]: m for m in meta}

def ym(s):  # "YYYY-MM" -> ordinal month
    y, m = map(int, s.split("-")); return y * 12 + (m - 1)
def lbl(v): return f"{v // 12}-{v % 12 + 1:02d}"

def activity(repo):
    out = subprocess.run(["git", "-C", f"../{repo}", "log",
                          "--date=format:%Y-%m", "--format=%ad"],
                         capture_output=True, text=True)
    months = [l for l in out.stdout.splitlines() if l.strip()]
    if not months:
        return [], [], 0, "", ""
    c = collections.Counter(months)
    keys = sorted(c)
    lo, hi = ym(keys[0]), ym(keys[-1])
    labels = [lbl(v) for v in range(lo, hi + 1)]
    values = [c.get(x, 0) for x in labels]
    return labels, values, sum(c.values()), keys[0], keys[-1]

JS = """
<script src="../vendor/echarts.min.js"></script>
<script>
(function(){
  var el=document.getElementById('activity');
  if(!window.echarts){ el.parentNode.style.display='none'; return; }
  var labels=__LABELS__, values=__VALUES__;
  if(!labels.length){ el.parentNode.style.display='none'; return; }
  var ch=echarts.init(el,null,{renderer:'canvas'});
  ch.setOption({backgroundColor:'transparent',
    grid:{left:42,right:16,top:14,bottom:56},
    tooltip:{trigger:'axis'},
    xAxis:{type:'category',data:labels,axisLabel:{color:'#8b949e',rotate:45,fontSize:10},axisLine:{lineStyle:{color:'#30363d'}}},
    yAxis:{type:'value',minInterval:1,axisLabel:{color:'#8b949e'},splitLine:{lineStyle:{color:'#21262d'}}},
    series:[{type:'bar',data:values,itemStyle:{color:'#58a6ff'},barMaxWidth:22}]});
  window.addEventListener('resize',function(){ch.resize();});
})();
</script>
"""

count = 0
for name, tag in taglines.items():
    md = f"docs/{name}.md"
    if not os.path.exists(md):
        continue
    m = metaby.get(name, {})
    vis = (m.get("visibility") or "").lower()
    lang = (m.get("primaryLanguage") or {}).get("name") or "—"
    url = m.get("url") or f"https://github.com/ScottYelich/{name}"
    site = f"https://scottyelich.github.io/{name}/"
    labels, values, total, first, last = activity(name)
    body = subprocess.run(["pandoc", md, "-f", "gfm", "-t", "html5"],
                          capture_output=True, text=True).stdout
    badge = f'<span class="badge {vis}">{vis}</span>' if vis else ""
    stats = " · ".join(filter(None, [
        html.escape(lang),
        f"{total} commits" if total else "",
        (f"{first} → {last}" if first else ""),
        f"report template v{TEMPLATE_VERSION}",
    ]))
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
  <div class="chart-card"><h3>Commit activity by month</h3><div id="activity"></div></div>
  <article class="markdown-body">
{body}
  </article>
  <footer class="foot">Report template v{TEMPLATE_VERSION} · generated {date} · <a href="{PORTFOLIO_URL}">ScottYelich · portfolio</a></footer>
</div>
"""
    js = JS.replace("__LABELS__", json.dumps(labels)).replace("__VALUES__", json.dumps(values))
    open(f"docs/{name}.html", "w", encoding="utf-8").write(head + js + "</body>\n</html>\n")
    count += 1
    print(f"  report: docs/{name}.html  ({total} commits)")

print(f"Generated {count} reports — template v{TEMPLATE_VERSION} @ {date}")

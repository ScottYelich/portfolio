#!/usr/bin/env python3
"""Replace the complexity / maturity / tests axes in data/scores.json with values
DERIVED from real repo signals (file count + size, commits + age, test-file ratio).
The other axes (value, reusability, autonomy, docs, llm) stay curated.

Run from the portfolio repo root:  python3 tools/derive-scores.py
Requires: gh (auth), git, sibling repos checked out at ../<name>.
"""
import json, subprocess, os, math, re, datetime

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(here))

def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout

meta = json.loads(sh("gh", "repo", "list", "ScottYelich", "--limit", "500",
                     "--json", "name,diskUsage") or "[]")
size = {m["name"]: m.get("diskUsage", 0) for m in meta}

doc = json.load(open("data/scores.json"))
names = [k for k in doc if not k.startswith("_")]
now = datetime.datetime.now(datetime.timezone.utc).timestamp()

raw = {}
for n in names:
    p = f"../{n}"
    commits = int((sh("git", "-C", p, "rev-list", "--count", "HEAD").strip() or "0"))
    files = [x for x in sh("git", "-C", p, "ls-files").splitlines() if x]
    nfiles = len(files)
    testf = sum(1 for f in files if re.search(r"(^|/)(tests?|spec)s?(/|_|\.|$)", f, re.I))
    ats = [int(x) for x in sh("git", "-C", p, "log", "--format=%at").split() if x.isdigit()]
    age_days = (now - min(ats)) / 86400 if ats else 0
    raw[n] = {
        # log-scaled so one huge repo doesn't compress everyone else
        "cplx": math.log10(nfiles + 1) + math.log10(max(size.get(n, 1), 1) + 1) * 0.5,
        # commits dominate; a small age bonus, capped so an old-but-empty repo stays low
        "mat":  math.log10(commits + 1) + min(age_days, 730) / 730.0 * 0.4,
        "testf": testf, "tratio": testf / max(nfiles, 1),
    }

def scaler(key, lo=8, hi=96):
    vals = [raw[n][key] for n in names]
    mn, mx = min(vals), max(vals)
    return lambda v: lo if mx == mn else round(lo + (v - mn) / (mx - mn) * (hi - lo))

sc_c, sc_m = scaler("cplx"), scaler("mat")
for n in names:
    doc[n]["complexity"] = sc_c(raw[n]["cplx"])
    doc[n]["maturity"]   = sc_m(raw[n]["mat"])
    doc[n]["tests"]      = 5 if raw[n]["testf"] == 0 else max(15, min(95, round(10 + raw[n]["tratio"] * 220)))

doc["_comment"] = ("Per-repo 0-100 scores. complexity/maturity/tests are DERIVED from real "
                   "signals (files+size, commits+age, test-file ratio) via tools/derive-scores.py; "
                   "value/reusability/autonomy/docs/llm are hand-curated. Single source of truth for "
                   "the radar (reports) and the index complexity x maturity chart.")

with open("data/scores.json", "w") as f:
    json.dump(doc, f, indent=0 if False else 2)
    f.write("\n")

print(f"{'repo':<15}{'cplx':>6}{'mat':>6}{'tests':>7}   (files / commits)")
for n in sorted(names, key=lambda x: -doc[x]["complexity"]):
    fc = len([x for x in sh('git','-C',f'../{n}','ls-files').splitlines() if x])
    cm = sh('git','-C',f'../{n}','rev-list','--count','HEAD').strip()
    print(f"{n:<15}{doc[n]['complexity']:>6}{doc[n]['maturity']:>6}{doc[n]['tests']:>7}   ({fc} / {cm})")

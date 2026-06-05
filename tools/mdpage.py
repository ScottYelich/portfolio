#!/usr/bin/env python3
"""Render a Markdown file into a self-contained, styled, browser-loadable HTML page.

Usage: mdpage.py <input.md> <output.html> <title> <repo-name> [portfolio-url]

Output is fully self-contained: readme.css is inlined with a provenance header
(source + version + date + sha256); markdown is pre-rendered by pandoc (no JS).
A top nav links back to the public portfolio.
"""
import sys, subprocess, hashlib, datetime, html, re, os

inp, out, title, repo = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
portfolio_url = sys.argv[5] if len(sys.argv) > 5 else "https://scottyelich.github.io/portfolio/"

here = os.path.dirname(os.path.abspath(__file__))
css_path = os.path.join(here, "..", "style", "readme.css")
css = open(css_path, encoding="utf-8").read()
sha = hashlib.sha256(css.encode("utf-8")).hexdigest()
m = re.search(r"@version\s+([0-9.]+)", css)
ver = m.group(1) if m else "0.1.0"
date = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

body = subprocess.run(["pandoc", inp, "-f", "gfm", "-t", "html5"],
                      capture_output=True, text=True, check=True).stdout

prov = (
    "/*! EMBEDDED ASSET — readme.css\n"
    " * source:  https://github.com/ScottYelich/portfolio/blob/main/style/readme.css\n"
    f" * version: {ver}\n * date:    {date}\n * sha256:  {sha}\n"
    " * note:    inlined for self-containment; check source for updates.\n */\n"
)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>
{prov}{css}</style>
</head>
<body>
<div class="wrap">
  <nav class="topbar">
    <a class="home" href="{html.escape(portfolio_url)}">← Portfolio</a>
    <span class="crumb">{html.escape(repo)}</span>
  </nav>
  <article class="markdown-body">
{body}
  </article>
  <footer class="foot">Part of <a href="{html.escape(portfolio_url)}">ScottYelich · portfolio</a> — the public starting point for these projects. Rendered {date}.</footer>
</div>
</body>
</html>
"""
with open(out, "w", encoding="utf-8") as f:
    f.write(page)
print(f"wrote {out} ({len(page)} bytes) from {inp}")

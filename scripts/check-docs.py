#!/usr/bin/env python3
"""Lightweight structural validation for PamPan's Universal Doc OS."""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]
required = ["index.html", "README.md", "AGENTS.md", "docs/README.md", "docs/manifest.yaml", "docs/assets/docs-style.css", "docs/reference/system-overview.html", "docs/reference/glossary.html", "docs/reference/startup-and-verification.html", "docs/handover/current.html", "docs/handover/changelog.html"]
errors=[]
for item in required:
    if not (ROOT/item).is_file(): errors.append(f"missing required file: {item}")
manifest=(ROOT/"docs/manifest.yaml").read_text() if (ROOT/"docs/manifest.yaml").exists() else ""
for path in re.findall(r"docs/[\w./-]+\.html", manifest):
    if not (ROOT/path).is_file(): errors.append(f"manifest path missing: {path}")
for path in (ROOT/"docs").rglob("*.html"):
    if "templates" in path.parts: continue
    text=path.read_text()
    relative=path.relative_to(ROOT).as_posix()
    for marker in ("<!doctype html>", "<main>", "<title>", "class=\"doc-nav\""):
        if marker not in text.lower() if marker == "<!doctype html>" else marker not in text:
            errors.append(f"{relative}: missing {marker}")
    for href in re.findall(r'(?:href|src)="([^"]+)"', text):
        if href.startswith(("http:", "https:", "#", "mailto:")): continue
        if not (path.parent / href).resolve().exists(): errors.append(f"{relative}: broken local link {href}")
if errors:
    print("Documentation validation failed:")
    print("\n".join(f"- {e}" for e in errors))
    sys.exit(1)
print("Documentation validation passed.")

#!/usr/bin/env python3
"""
lint_docs.py — quality linter for generated documentation.

Part of the doc-generator extension. Pure standard library (no installs).
Scans generated Markdown docs and reports deterministic quality issues so a
half-filled template, leftover placeholder, or Confluence-breaking HTML never
ships unnoticed. It does NOT judge prose or detect fabrication — those stay a
human review.

Usage:
    python3 docs/tools/lint_docs.py [path ...]      # default: docs/generated

Exit code: 0 if no ERRORs, 1 if any ERROR found (WARN/INFO never fail).
"""
import sys, os, re, glob

# files that are not deliverables
SKIP_NAMES = {"README.md"}

def find_docs(paths):
    out = []
    for p in paths:
        if os.path.isdir(p):
            out += glob.glob(os.path.join(p, "**", "*.md"), recursive=True)
        elif p.endswith(".md"):
            out.append(p)
    return sorted(set(f for f in out if os.path.basename(f) not in SKIP_NAMES))

def lint(path):
    """Return list of (level, message). level in ERROR/WARN/INFO."""
    issues = []
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()

    # ERROR: unfilled template placeholders
    ph = sorted(set(re.findall(r"\{\{[^}]+\}\}", text)))
    if ph:
        issues.append(("ERROR", f"unfilled template placeholder(s): {', '.join(ph[:6])}"
                       + (" …" if len(ph) > 6 else "")))

    # ERROR: raw HTML that Confluence escapes / breaks our convention
    html = sorted(set(re.findall(r"<\s*/?\s*(mark|table|td|tr|th)\b", text, re.I)))
    if html:
        issues.append(("ERROR", f"raw HTML tag(s) (use markdown + ✅/– instead): "
                       f"{', '.join('<'+h+'>' for h in html)}"))
    if re.search(r"\bstyle\s*=", text):
        issues.append(("ERROR", "inline style= attribute (escaped by Confluence)"))

    # ERROR: leftover template guidance comments
    if re.search(r"<!--\s*guidance:", text, re.I):
        issues.append(("ERROR", "leftover <!-- guidance: … --> comment from template"))

    # ERROR: no version-history row (matches `| 1.0 |` style)
    if not re.search(r"^\|\s*\d+\.\d+\s*\|", text, re.M):
        issues.append(("ERROR", "no Version history row found (e.g. `| 1.0 | … |`)"))

    # WARN: highlighting legend missing (a line containing both 🟡 and 🔴)
    if not any(("🟡" in ln and "🔴" in ln) for ln in lines):
        issues.append(("WARN", "highlighting legend line (🟡 … 🔴) not found near top"))

    # WARN: author still a placeholder
    if "🟡 [Author]" in text or "[Author]" in text:
        issues.append(("WARN", "author is still a placeholder (🟡 [Author])"))

    # WARN: other HTML comments (review before publishing)
    n_comments = len(re.findall(r"<!--(?!\s*guidance:).*?-->", text, re.S))
    if n_comments:
        issues.append(("WARN", f"{n_comments} HTML comment(s) present — review before publishing"))

    # WARN: empty section — a heading with no body AND no subsections.
    # (A parent heading followed by a deeper subheading is NOT empty.)
    heads = [(i, ln) for i, ln in enumerate(lines) if re.match(r"^#{1,6}\s", ln)]
    def hlevel(ln):
        return len(re.match(r"^(#{1,6})", ln).group(1))
    for idx in range(len(heads) - 1):
        i, h = heads[idx]
        j, nh = heads[idx + 1]
        body = "\n".join(lines[i + 1:j]).strip()
        if not body and hlevel(nh) <= hlevel(h):
            issues.append(("WARN", f"empty section: '{h.strip()}'"))

    # INFO: screenshot / file placeholders still present (allowed)
    n_img = len(re.findall(r"🖼️", text))
    n_file = len(re.findall(r"📄", text))
    if n_img or n_file:
        issues.append(("INFO", f"{n_img} screenshot + {n_file} file placeholder(s) (not yet captured)"))

    return issues

def main():
    paths = sys.argv[1:] or ["docs/generated"]
    docs = find_docs(paths)
    if not docs:
        print("No generated docs found under:", ", ".join(paths))
        return 0
    total = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for f in docs:
        issues = lint(f)
        if not issues:
            print(f"✓ {f}")
            continue
        print(f"• {f}")
        for level, msg in sorted(issues, key=lambda x: ["ERROR","WARN","INFO"].index(x[0])):
            mark = {"ERROR": "✗ ERROR", "WARN": "⚠ WARN", "INFO": "  info"}[level]
            print(f"    {mark}: {msg}")
            total[level] += 1
    print(f"\n{len(docs)} doc(s) — {total['ERROR']} error, {total['WARN']} warn, {total['INFO']} info")
    return 1 if total["ERROR"] else 0

if __name__ == "__main__":
    sys.exit(main())

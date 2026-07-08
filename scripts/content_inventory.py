#!/usr/bin/env python3
"""Content inventory — the deterministic seed for the weekly content review.

Lists every reader-facing content page with its word count, last-modified date, and
age, and flags the thin and the stale. The content curator
(`.claude/agents/content-curator.md`) starts from this instead of reading the whole
corpus every week — deterministic-first: a script does the cheap survey so the model
spends its judgment on the one page worth improving.

Usage:
    python3 scripts/content_inventory.py            # full table, newest-neglected first
    python3 scripts/content_inventory.py --thin     # only pages under the thin threshold
    python3 scripts/content_inventory.py --stale    # only pages past the stale threshold
    python3 scripts/content_inventory.py --focus    # the shortlist a weekly run should pick from
    python3 scripts/content_inventory.py --json      # machine-readable (for the curator)
"""
from __future__ import annotations

import argparse
import datetime
import glob
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (section label, glob) — the content a review should police.
SECTIONS = [
    ("posts/corp", "pages/_posts/corp/*.md"),
    ("posts/erp", "pages/_posts/erp/*.md"),
    ("posts/muses", "pages/_posts/muses/*.md"),
    ("posts/tech", "pages/_posts/tech/*.md"),
    ("services", "pages/_services/*.md"),
    ("toolkit", "pages/_toolkit/*.md"),
    ("case-studies", "pages/_case-studies/*.md"),
]
ROOT_PAGES = ["about.md", "ai-operations.md"]  # substantive prose; not utility/hub pages

# Heuristics that seed the curator's choice — not hard rules.
THIN_WORDS = 700          # a post/service under this is a candidate to expand
STALE_DAYS = 180          # a page untouched this long is a candidate to refresh

_FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
_LASTMOD_RE = re.compile(r"^lastmod:\s*(\d{4}-\d{2}-\d{2})", re.M)
_DATE_RE = re.compile(r"^date:\s*(\d{4}-\d{2}-\d{2})", re.M)
_TITLE_RE = re.compile(r'^title:\s*"?(.+?)"?\s*$', re.M)
_LAYOUT_RE = re.compile(r"^layout:\s*(\S+)", re.M)


def _body_words(text: str) -> int:
    body = _FM_RE.sub("", text, count=1)
    return len(re.findall(r"\w+", body))


def inventory(today: datetime.date) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()

    def add(path: Path, section: str):
        rel = path.relative_to(ROOT).as_posix()
        if rel in seen:
            return
        seen.add(rel)
        text = path.read_text(encoding="utf-8", errors="replace")
        fm_match = _FM_RE.match(text)
        fm = fm_match.group(1) if fm_match else ""
        # Skip structural pages that are short by design, not by neglect:
        # section-landing stubs, collection index pages, and loop landings
        # (frontmatter `landing: true`). These aren't articles to expand.
        layout = (_LAYOUT_RE.search(fm) or [None, ""])[1] if fm else ""
        words = _body_words(text)
        is_landing = bool(re.search(r"^landing:\s*true\b", fm, re.M)) if fm else False
        if layout == "section" or words == 0 or path.name == "index.md" or is_landing:
            return
        lm = _LASTMOD_RE.search(fm) or _DATE_RE.search(fm)
        lastmod = lm.group(1) if lm else None
        age = None
        if lastmod:
            try:
                age = (today - datetime.date.fromisoformat(lastmod)).days
            except ValueError:
                age = None
        title_m = _TITLE_RE.search(fm)
        rows.append({
            "path": rel,
            "section": section,
            "title": title_m.group(1).strip() if title_m else "",
            "words": words,
            "lastmod": lastmod,
            "age_days": age,
            "thin": words < THIN_WORDS,
            "stale": age is not None and age > STALE_DAYS,
        })

    for section, pattern in SECTIONS:
        for p in sorted(ROOT.glob(pattern)):
            add(p, section)
    for name in ROOT_PAGES:
        p = ROOT / name
        if p.exists():
            add(p, "root")
    return rows


def _staleness_key(r: dict):
    # Surface the neglected and the thin first: oldest age, then fewest words.
    return (-(r["age_days"] or 0), r["words"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Content inventory for the weekly review.")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    parser.add_argument("--thin", action="store_true", help="only pages under the thin threshold")
    parser.add_argument("--stale", action="store_true", help="only pages past the stale threshold")
    parser.add_argument("--focus", action="store_true", help="the shortlist a weekly run should pick from")
    parser.add_argument("--today", help="override today's date (YYYY-MM-DD) for reproducibility")
    args = parser.parse_args()

    today = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
    rows = inventory(today)

    if args.thin:
        rows = [r for r in rows if r["thin"]]
    if args.stale:
        rows = [r for r in rows if r["stale"]]
    if args.focus:
        # The candidates worth a human/AI look: thin or stale, worst first.
        rows = [r for r in rows if r["thin"] or r["stale"]]

    rows.sort(key=_staleness_key)

    if args.json:
        print(json.dumps(rows, indent=2))
        return 0

    print(f"content_inventory: {len(rows)} page(s)  "
          f"(thin < {THIN_WORDS}w, stale > {STALE_DAYS}d, as of {today})\n")
    print(f"  {'words':>5}  {'age':>5}  {'flags':<10}  section / path")
    for r in rows:
        flags = ("thin " if r["thin"] else "") + ("stale" if r["stale"] else "")
        age = f"{r['age_days']}d" if r["age_days"] is not None else "  ?"
        print(f"  {r['words']:5d}  {age:>5}  {flags:<10}  {r['section']}  {r['path']}")
    thin = sum(1 for r in rows if r["thin"])
    stale = sum(1 for r in rows if r["stale"])
    print(f"\ncontent_inventory: {thin} thin, {stale} stale")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

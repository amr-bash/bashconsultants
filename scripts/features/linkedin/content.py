"""Map a Jekyll post's frontmatter to a LinkedIn article share.

Reuses the frontmatter reader and banned-phrase list from
scripts/content_lint.py so the two stay in lockstep; falls back to a local
minimal reader when run in isolation. Builds the canonical URL, resolves the
`preview` image to its file on disk, and seeds default commentary.

Stdlib only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from config import COMMENTARY_MAX, FALLBACK_IMAGE, PREVIEWS_DIR, REPO_ROOT

# --- Reuse content_lint internals when available ---------------------------
# Append (not insert) so this package's own modules keep priority on sys.path.
sys.path.append(str(Path(__file__).resolve().parents[2]))  # .../scripts
try:
    from content_lint import (  # type: ignore
        BANNED_PATTERNS,
        FILENAME_DATE_RE,
        parse_frontmatter,
        split_frontmatter,
    )
except Exception:  # pragma: no cover - isolation fallback
    FILENAME_DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})-")
    BANNED_PATTERNS = []

    def split_frontmatter(text):
        if not text.startswith("---"):
            return None, text, 1
        lines = text.split("\n")
        for idx in range(1, len(lines)):
            if lines[idx].strip() == "---":
                return "\n".join(lines[1:idx]), "\n".join(lines[idx + 1:]), idx + 2
        return None, text, 1

    def parse_frontmatter(fm_text):
        data, key_lines = {}, {}
        key_re = re.compile(r"^([A-Za-z0-9_-]+):\s*(.*?)\s*$")
        for i, line in enumerate(fm_text.split("\n")):
            m = key_re.match(line)
            if not m:
                continue
            key, val = m.group(1), m.group(2).strip()
            key_lines[key] = i + 1
            if val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                data[key] = [p.strip().strip("\"'") for p in inner.split(",") if p.strip()]
            else:
                data[key] = val.strip("\"'")
        return data, key_lines

POSTS_ROOT = REPO_ROOT / "pages" / "_posts"

# Acronyms that read better upper-cased as hashtags.
_ACRONYMS = {"ai", "mcp", "erp", "crm", "bi", "saas", "iaas", "smb", "it",
             "api", "ci", "cd", "kpi", "roi", "sql", "hr"}


class Post:
    def __init__(self, path, data):
        self.path = Path(path)
        self.data = data

    def get(self, key, default=""):
        val = self.data.get(key, default)
        return val if isinstance(val, str) else default

    @property
    def title(self):
        return self.get("title")

    @property
    def description(self):
        return self.get("description")

    @property
    def tags(self):
        tags = self.data.get("tags", [])
        return tags if isinstance(tags, list) else []


def find_post(ref):
    """Resolve a post reference to a file path.

    Accepts a path to a .md file, `section/YYYY-MM-DD-slug`, `YYYY-MM-DD-slug`,
    or a bare slug. Raises FileNotFoundError with a helpful message otherwise.
    """
    direct = Path(ref)
    if direct.suffix == ".md" and direct.exists():
        return direct.resolve()
    if (REPO_ROOT / ref).exists() and (REPO_ROOT / ref).suffix == ".md":
        return (REPO_ROOT / ref).resolve()

    norm = ref.strip().rstrip("/")
    if norm.endswith(".md"):
        norm = norm[:-3]
    base = norm.split("/")[-1]
    for cand in sorted(POSTS_ROOT.glob("**/*.md")):
        stem = cand.stem
        rel_noext = str(cand.relative_to(POSTS_ROOT))[:-3]
        slug = FILENAME_DATE_RE.sub("", stem)
        if norm in (rel_noext, stem, slug) or base in (stem, slug):
            return cand.resolve()
    raise FileNotFoundError(
        f"no post matches '{ref}' under {POSTS_ROOT.relative_to(REPO_ROOT)} "
        "(try section/YYYY-MM-DD-slug or the slug)"
    )


def load_post(ref):
    path = find_post(ref)
    text = path.read_text(encoding="utf-8")
    fm_text, _body, _start = split_frontmatter(text)
    if fm_text is None:
        raise ValueError(f"{path} has no frontmatter")
    data, _lines = parse_frontmatter(fm_text)
    return Post(path, data)


def canonical_url(cfg, path):
    """Build the production URL: {base}/posts/{Y}/{M}/{D}/{slug}/.

    The section subfolder is intentionally dropped — it does not appear in the
    Jekyll permalink (collections.posts.permalink = /:collection/:year/:month/:day/:slug/).
    """
    name = Path(path).name
    m = FILENAME_DATE_RE.match(name)
    if not m:
        raise ValueError(f"cannot derive date from filename: {name}")
    year, month, day = m.group(1).split("-")
    slug = FILENAME_DATE_RE.sub("", Path(path).stem)
    return f"{cfg.base_url}/posts/{year}/{month}/{day}/{slug}/"


def resolve_thumbnail(preview):
    """Resolve a `preview:` frontmatter value to a file on disk.

    All previews live in assets/images/previews/, so match by basename. Falls
    back to the site-wide og_image, then None (post without a thumbnail).
    """
    if preview:
        candidate = PREVIEWS_DIR / Path(preview).name
        if candidate.exists():
            return candidate
    if FALLBACK_IMAGE.exists():
        return FALLBACK_IMAGE
    return None


def tags_to_hashtags(tags, limit=3):
    out = []
    for tag in tags[:limit]:
        tokens = re.split(r"[\s_-]+", str(tag).strip())
        parts = []
        for tok in tokens:
            if not tok:
                continue
            parts.append(tok.upper() if tok.lower() in _ACRONYMS else tok.capitalize())
        if parts:
            out.append("#" + "".join(parts))
    return " ".join(out)


def default_commentary(cfg, post):
    """A safe, brand-neutral commentary seed for an article share.

    Uses the post's sub-title/excerpt as the hook (the card already carries the
    description), plus a few hashtags. Kept minimal so Model A stays on-brand
    without a human; Model B replaces this with human-approved copy.
    """
    hook = (post.get("sub-title") or post.get("subtitle")
            or post.get("excerpt") or post.description).strip()
    hashtags = tags_to_hashtags(post.tags)
    parts = [hook] if hook else []
    if hashtags:
        parts.append(hashtags)
    text = "\n\n".join(parts)
    return text[:COMMENTARY_MAX]


def guard_commentary(text):
    """Return a list of (level, message) problems with proposed commentary.

    'error' problems (banned phrase, over length) should block a live post
    unless forced; 'warning' problems are advisory. This is the mechanical half
    of the brand gate — the human review before merge is the other half.
    """
    problems = []
    if len(text) > COMMENTARY_MAX:
        problems.append(("error", f"commentary is {len(text)} chars (max {COMMENTARY_MAX})"))
    for name, pattern in BANNED_PATTERNS:
        m = pattern.search(text)
        if m:
            problems.append(("error", f'banned phrase "{m.group(0)}" ({name})'))
    if "!" in text:
        problems.append(("warning", "exclamation mark in commentary (house style: none)"))
    return problems

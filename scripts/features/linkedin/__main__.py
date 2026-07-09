#!/usr/bin/env python3
"""LinkedIn company-page publisher for bashconsultants.com.

Governed pipeline: agents draft commentary, a human approves it (by merging a
draft under drafts/linkedin/), and this script does the mechanical publish to
the company page. Deterministic, stdlib-only, dry-run-first.

Run as a directory so imports resolve with zero setup:

    python3 scripts/features/linkedin <command> [options]

Commands:
    post-article <ref>   Share a blog post as an article (link) card.
    post-text            Post a standalone text update.
    from-drafts          Publish every approved draft in drafts/linkedin/.
    refresh-token        Refresh the access token (needs refresh creds).
    check-token          Validate the token and warn before the 60-day expiry.
    verify --urn <urn>   Fetch a published post back from LinkedIn.
    self-test            Build payloads offline and assert their shape.

Secrets come from the environment only (LINKEDIN_ACCESS_TOKEN, and optionally
LINKEDIN_REFRESH_TOKEN + LINKEDIN_CLIENT_ID + LINKEDIN_CLIENT_SECRET). See
.env.example and docs/automation.md.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import auth
import content
import ledger
import posts
from config import COMMENTARY_MAX, QUEUE_DIR, REPO_ROOT, Config
from net import LinkedInHTTPError


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_config(args):
    return Config(base_url=args.base_url, org_urn=args.org_urn,
                  api_version=args.api_version)


def _print_json(obj):
    print(json.dumps(obj, indent=2, ensure_ascii=False))


def _report_guard(problems, *, force, dry_run):
    """Print guard problems; return True only if a LIVE post must be blocked.

    Dry runs always render (return False) so authors can preview the payload;
    live posts block on any error-level problem unless --force.
    """
    has_error = False
    for level, msg in problems:
        print(f"  [{level.upper()}] {msg}")
        if level == "error":
            has_error = True
    if has_error and not force and not dry_run:
        print("guard: refusing to post (fix the commentary or pass --force).")
        return True
    return False


def _read_commentary(args):
    if getattr(args, "commentary_file", None):
        return Path(args.commentary_file).read_text(encoding="utf-8").strip()
    if getattr(args, "commentary", None):
        return args.commentary
    return None


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_post_article(cfg, args):
    post = content.load_post(args.ref)
    url = content.canonical_url(cfg, post.path)
    title, description = post.title, post.description
    if not title or not description:
        print(f"error: post is missing title/description ({post.path})")
        return 1

    commentary = _read_commentary(args) or content.default_commentary(cfg, post)
    thumb = None if args.no_thumbnail else content.resolve_thumbnail(post.get("preview"))
    source_file = str(post.path.relative_to(REPO_ROOT))

    print(f"article: {source_file}")
    print(f"  url:   {url}")
    print(f"  card:  {title} — {description}")
    if thumb:
        print(f"  thumb: {thumb.relative_to(REPO_ROOT)} ({thumb.stat().st_size} bytes)")
    else:
        print("  thumb: (none — posting without a card image)")
    print("  commentary:")
    for line in commentary.splitlines() or [""]:
        print(f"    | {line}")

    problems = content.guard_commentary(commentary)
    if problems:
        print("  guard:")
        if _report_guard(problems, force=args.force, dry_run=args.dry_run):
            return 1

    existing = ledger.get_entry(cfg, url)
    if existing and existing.get("linkedin_urn") and not args.force:
        print(f"skip: already shared as {existing['linkedin_urn']} on {existing.get('posted_at')}")
        return 0

    payload = posts.build_article_payload(
        cfg, url=url, title=title, description=description,
        commentary=commentary, thumbnail_urn=None)

    if args.dry_run:
        print("dry-run: payload that would POST to /rest/posts "
              "(thumbnail URN filled in at publish):")
        _print_json(payload)
        return 0

    token = auth.resolve_token(cfg, verbose=args.verbose)
    thumb_urn = None
    if thumb:
        try:
            import images
            thumb_urn = images.upload_image(cfg, token, thumb, verbose=args.verbose)
            payload["content"]["article"]["thumbnail"] = thumb_urn
        except Exception as exc:  # thumbnail is optional — warn and continue
            print(f"warning: thumbnail upload failed ({exc}); posting without image")
    urn = posts.create_post(cfg, token, payload)
    ledger.record(cfg, url, urn, source_file=source_file,
                  image_urn=thumb_urn, kind="article")
    print(f"published: {urn}")
    print(f"  {posts.feed_url(urn)}")
    return 0


def cmd_post_text(cfg, args):
    if args.message_file:
        message = Path(args.message_file).read_text(encoding="utf-8").strip()
    else:
        message = args.message
    if not message:
        print("error: empty message")
        return 1

    print("text update:")
    for line in message.splitlines():
        print(f"  | {line}")
    problems = content.guard_commentary(message)
    if problems:
        print("guard:")
        if _report_guard(problems, force=args.force, dry_run=args.dry_run):
            return 1

    payload = posts.build_text_payload(cfg, message)
    if args.dry_run:
        print("dry-run: payload that would POST to /rest/posts:")
        _print_json(payload)
        return 0

    token = auth.resolve_token(cfg, verbose=args.verbose)
    urn = posts.create_post(cfg, token, payload)
    print(f"published: {urn}")
    print(f"  {posts.feed_url(urn)}")
    return 0


def cmd_from_drafts(cfg, args):
    if not QUEUE_DIR.exists():
        print(f"no draft queue at {QUEUE_DIR.relative_to(REPO_ROOT)} — nothing to do")
        return 0
    drafts = sorted(QUEUE_DIR.glob("*.md"))
    if not drafts:
        print("draft queue is empty")
        return 0

    failures = 0
    for path in drafts:
        data, body = _read_draft(path)
        status = str(data.get("status", "pending")).lower()
        if status != "pending":
            if args.verbose:
                print(f"skip {path.name}: status={status}")
            continue
        kind = str(data.get("type", "article")).lower()
        commentary = body.strip() or str(data.get("commentary", ""))
        print(f"\n--- {path.name} ({kind}) ---")
        rc = 0
        if kind == "article":
            sub = argparse.Namespace(
                ref=str(data.get("source", "")), commentary=commentary,
                commentary_file=None, no_thumbnail=bool(data.get("no_thumbnail")),
                force=args.force, dry_run=args.dry_run, verbose=args.verbose)
            rc = cmd_post_article(cfg, sub)
        elif kind in ("update", "text"):
            sub = argparse.Namespace(
                message=commentary, message_file=None, force=args.force,
                dry_run=args.dry_run, verbose=args.verbose)
            rc = cmd_post_text(cfg, sub)
        else:
            print(f"  error: unknown draft type '{kind}'")
            rc = 1
        if rc != 0:
            failures += 1
        elif not args.dry_run:
            _mark_published(path)
    return 1 if failures else 0


def cmd_refresh_token(cfg, args):
    data = auth.refresh(cfg)
    print("refresh-token: ok — new access token obtained (expiry recorded in ledger).")
    if args.write_env:
        _update_env({"LINKEDIN_ACCESS_TOKEN": data.get("access_token", ""),
                     **({"LINKEDIN_REFRESH_TOKEN": data["refresh_token"]}
                        if data.get("refresh_token") else {})})
        print("refresh-token: wrote new token(s) to .env (mode 600).")
    else:
        print("refresh-token: token not written anywhere. Use --write-env locally, "
              "or update the LINKEDIN_ACCESS_TOKEN secret in CI.")
    return 0


def cmd_check_token(cfg, args):
    return auth.check(cfg, warn_days=args.warn_days, verbose=args.verbose)


def cmd_verify(cfg, args):
    token = auth.resolve_token(cfg, verbose=args.verbose)
    data = posts.get_post(cfg, token, args.urn)
    _print_json({k: data.get(k) for k in
                 ("id", "author", "lifecycleState", "visibility", "commentary", "content")
                 if k in data})
    return 0


# ---------------------------------------------------------------------------
# Draft-queue file helpers
# ---------------------------------------------------------------------------

def _read_draft(path):
    text = path.read_text(encoding="utf-8")
    fm_text, body, _ = content.split_frontmatter(text)
    if fm_text is None:
        return {}, text
    data, _lines = content.parse_frontmatter(fm_text)
    return data, body


def _mark_published(path):
    """Flip status: pending -> published in a draft file, in place."""
    lines = path.read_text(encoding="utf-8").splitlines()
    out = []
    replaced = False
    for line in lines:
        if not replaced and line.strip().lower().startswith("status:"):
            out.append("status: published")
            replaced = True
        else:
            out.append(line)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def _update_env(pairs):
    env_path = REPO_ROOT / ".env"
    lines = env_path.read_text(encoding="utf-8").splitlines() if env_path.exists() else []
    keys = set(pairs)
    out, seen = [], set()
    for line in lines:
        key = line.split("=", 1)[0].strip() if "=" in line else None
        if key in keys:
            out.append(f"{key}={pairs[key]}")
            seen.add(key)
        else:
            out.append(line)
    for key in keys - seen:
        out.append(f"{key}={pairs[key]}")
    env_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    os.chmod(env_path, 0o600)


# ---------------------------------------------------------------------------
# Offline self-test
# ---------------------------------------------------------------------------

def cmd_self_test(cfg, args):
    failures = []

    # Canonical URL derivation from a filename.
    fake = Path("pages/_posts/tech/2026-07-06-mcp-for-the-back-office.md")
    got = content.canonical_url(cfg, fake)
    want = f"{cfg.base_url}/posts/2026/07/06/mcp-for-the-back-office/"
    if got != want:
        failures.append(f"canonical_url: got {got}, want {want}")

    # Article payload shape.
    payload = posts.build_article_payload(
        cfg, url=want, title="T", description="D",
        commentary="hello #AI", thumbnail_urn="urn:li:image:123")
    checks = {
        "author == org urn": payload["author"] == cfg.org_urn,
        "lifecycleState PUBLISHED": payload["lifecycleState"] == "PUBLISHED",
        "visibility PUBLIC": payload["visibility"] == "PUBLIC",
        "feedDistribution MAIN_FEED": payload["distribution"]["feedDistribution"] == "MAIN_FEED",
        "article.source set": payload["content"]["article"]["source"] == want,
        "article.thumbnail set": payload["content"]["article"]["thumbnail"] == "urn:li:image:123",
    }
    for name, ok in checks.items():
        if not ok:
            failures.append(f"article payload: {name} failed")

    # Text payload has no content key.
    text_payload = posts.build_text_payload(cfg, "just text")
    if "content" in text_payload:
        failures.append("text payload should not carry a content key")

    # Hashtag mapping + banned-phrase guard.
    if content.tags_to_hashtags(["mcp", "back-office", "ai"]) != "#MCP #BackOffice #AI":
        failures.append(f"hashtags: got {content.tags_to_hashtags(['mcp', 'back-office', 'ai'])}")
    if content.BANNED_PATTERNS:
        problems = content.guard_commentary("this is a world-class revolutionary post")
        if not any(lvl == "error" for lvl, _ in problems):
            failures.append("guard: banned phrases not caught")
    if not any(lvl == "error" for lvl, _ in content.guard_commentary("x" * (COMMENTARY_MAX + 1))):
        failures.append("guard: over-length commentary not caught")

    if failures:
        print("self-test: FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("self-test: PASS (payload shape, canonical URL, hashtags, brand guard)")
    return 0


# ---------------------------------------------------------------------------
# Argument parsing
# ---------------------------------------------------------------------------

def build_parser():
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--dry-run", action="store_true",
                        help="render the payload; make no API calls, write no ledger")
    common.add_argument("--verbose", action="store_true")
    common.add_argument("--base-url", default=None, help="override the canonical host")
    common.add_argument("--org-urn", default=None, help="override the organization URN")
    common.add_argument("--api-version", default=None, help="override LinkedIn-Version (YYYYMM)")
    common.add_argument("--force", action="store_true",
                        help="ignore the ledger / guard errors and post anyway")

    parser = argparse.ArgumentParser(prog="linkedin", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("post-article", parents=[common], help="share a blog post")
    p.add_argument("ref", help="post reference: section/YYYY-MM-DD-slug, a path, or a slug")
    p.add_argument("--commentary", help="commentary text (default: derived from frontmatter)")
    p.add_argument("--commentary-file", help="read commentary from a file")
    p.add_argument("--no-thumbnail", action="store_true", help="post without a card image")
    p.set_defaults(func=cmd_post_article)

    p = sub.add_parser("post-text", parents=[common], help="post a standalone update")
    grp = p.add_mutually_exclusive_group(required=True)
    grp.add_argument("--message", help="the update text")
    grp.add_argument("--message-file", help="read the update text from a file")
    p.set_defaults(func=cmd_post_text)

    p = sub.add_parser("from-drafts", parents=[common],
                       help="publish approved drafts in drafts/linkedin/")
    p.set_defaults(func=cmd_from_drafts)

    p = sub.add_parser("refresh-token", parents=[common], help="refresh the access token")
    p.add_argument("--write-env", action="store_true", help="write the new token to .env (local)")
    p.set_defaults(func=cmd_refresh_token)

    p = sub.add_parser("check-token", parents=[common], help="validate token, warn near expiry")
    p.add_argument("--warn-days", type=int, default=7)
    p.set_defaults(func=cmd_check_token)

    p = sub.add_parser("verify", parents=[common], help="fetch a post back by URN")
    p.add_argument("--urn", required=True)
    p.set_defaults(func=cmd_verify)

    p = sub.add_parser("self-test", parents=[common], help="offline payload/shape checks")
    p.set_defaults(func=cmd_self_test)

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    cfg = make_config(args)
    try:
        return args.func(cfg, args)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}")
        return 1
    except LinkedInHTTPError as exc:
        print(f"LinkedIn API error: {exc}")
        if exc.body and args.verbose:
            _print_json(exc.body)
        return 1


if __name__ == "__main__":
    sys.exit(main())

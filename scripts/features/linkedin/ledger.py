"""Idempotency ledger for the LinkedIn publisher.

A single JSON file at .github/linkedin-log.json maps each shared canonical URL to
its LinkedIn post URN, so a source is never posted twice. It lives under
.github/ (not _data/) so writing it does NOT trigger a Jekyll rebuild and needs
no hand-emitted YAML.

Keyed by canonical URL (stable even if a post file moves between sections). Keys
beginning with "_" are metadata (e.g. "_token"), not shares.

Stdlib only.
"""

from __future__ import annotations

import datetime
import json
import os
import tempfile

from config import LEDGER_PATH

_TOKEN_KEY = "_token"


def load(cfg):
    path = LEDGER_PATH
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return {}


def _save(cfg, data):
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Atomic write so a killed run never leaves a half-written ledger.
    fd, tmp = tempfile.mkstemp(dir=str(LEDGER_PATH.parent), suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, LEDGER_PATH)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def is_posted(cfg, url):
    entry = load(cfg).get(url)
    return bool(entry and entry.get("linkedin_urn"))


def get_entry(cfg, url):
    return load(cfg).get(url)


def record(cfg, url, urn, *, source_file=None, image_urn=None, kind="article"):
    data = load(cfg)
    data[url] = {
        "linkedin_urn": urn,
        "posted_at": _utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "type": kind,
    }
    if source_file:
        data[url]["source_file"] = source_file
    if image_urn:
        data[url]["image_urn"] = image_urn
    _save(cfg, data)
    return data[url]


def set_token_expiry(cfg, iso):
    data = load(cfg)
    meta = data.get(_TOKEN_KEY, {})
    meta["expires_at"] = iso
    data[_TOKEN_KEY] = meta
    _save(cfg, data)


def get_token_expiry(cfg):
    meta = load(cfg).get(_TOKEN_KEY) or {}
    return meta.get("expires_at")


def _utcnow():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

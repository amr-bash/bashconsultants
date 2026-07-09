"""Minimal urllib client for the PostHog REST API.

Bearer auth with the personal API key, JSON encode/decode, and retry on 429/5xx.
The token is never written to stdout, stderr, or an exception message. Stdlib
only. Named net.py (not http.py) to avoid shadowing the stdlib `http` package.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

_RETRY = {429, 500, 502, 503, 504}
_MAX_RETRIES = 3


class PostHogHTTPError(Exception):
    def __init__(self, status, message, body=None):
        self.status = status
        self.body = body
        super().__init__(f"HTTP {status}: {message}")


def request(method, url, token, *, json_body=None, expect_json=True, timeout=30):
    """Return (status, headers, parsed_body). Raise PostHogHTTPError on non-2xx."""
    data = json.dumps(json_body).encode("utf-8") if json_body is not None else None
    headers = {"Authorization": f"Bearer {token}"}
    if data is not None:
        headers["Content-Type"] = "application/json"

    attempt = 0
    while True:
        attempt += 1
        req = urllib.request.Request(url, data=data, method=method, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                parsed = json.loads(raw) if (expect_json and raw) else raw
                return resp.status, dict(resp.headers.items()), parsed
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace") if exc.fp else ""
            if exc.code in _RETRY and attempt <= _MAX_RETRIES:
                time.sleep(min(2 ** attempt, 20))
                continue
            message, body = _parse_error(raw)
            raise PostHogHTTPError(exc.code, message, body)
        except urllib.error.URLError as exc:
            if attempt <= _MAX_RETRIES:
                time.sleep(min(2 ** attempt, 20))
                continue
            raise PostHogHTTPError(0, f"network error: {exc.reason}")


def _parse_error(raw):
    try:
        body = json.loads(raw)
        return body.get("detail") or body.get("message") or "request failed", body
    except ValueError:
        return raw[:300] or "request failed", None

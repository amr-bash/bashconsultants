"""Tiny urllib-based HTTP client for the LinkedIn REST API.

Centralizes the LinkedIn request contract (bearer auth, the
`X-Restli-Protocol-Version` and `LinkedIn-Version` headers), JSON encode/decode,
and retry/backoff on 429 and 5xx. The access token is never written to stdout,
stderr, or an exception message.

Stdlib only.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

from config import RESTLI_VERSION

_RETRY_STATUSES = {429, 500, 502, 503, 504}
_MAX_RETRIES = 3


class LinkedInHTTPError(Exception):
    """A non-2xx response from LinkedIn after retries.

    `body` holds the parsed error payload (dict) when available. The request's
    bearer token is never included here.
    """

    def __init__(self, status, message, body=None, request_id=None):
        self.status = status
        self.body = body
        self.request_id = request_id
        detail = f" (x-li-uuid={request_id})" if request_id else ""
        super().__init__(f"HTTP {status}: {message}{detail}")


def linkedin_headers(token, api_version, *, restli=True, extra=None):
    """Standard headers for a LinkedIn REST call."""
    headers = {
        "Authorization": f"Bearer {token}",
        "LinkedIn-Version": str(api_version),
        "Content-Type": "application/json",
    }
    if restli:
        headers["X-Restli-Protocol-Version"] = RESTLI_VERSION
    if extra:
        headers.update(extra)
    return headers


def _safe_error(status, raw, exc=None):
    """Build a LinkedInHTTPError from a response body without leaking secrets."""
    body = None
    message = "request failed"
    request_id = None
    if raw:
        try:
            body = json.loads(raw)
            message = body.get("message") or body.get("error_description") or message
            request_id = body.get("serviceErrorCode") or body.get("code")
        except (ValueError, AttributeError):
            message = raw[:300]
    if exc is not None and hasattr(exc, "headers") and exc.headers:
        request_id = exc.headers.get("x-li-uuid") or request_id
    return LinkedInHTTPError(status, message, body=body, request_id=request_id)


def request(method, url, *, headers=None, json_body=None, raw_body=None,
            expect_json=True, timeout=30):
    """Perform an HTTP request with retry/backoff.

    Returns (status, response_headers, parsed_or_bytes). Raises
    LinkedInHTTPError on a non-2xx status once retries are exhausted.
    """
    data = None
    if json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
    elif raw_body is not None:
        data = raw_body

    attempt = 0
    while True:
        attempt += 1
        req = urllib.request.Request(url, data=data, method=method,
                                     headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = resp.status
                resp_headers = dict(resp.headers.items())
                raw = resp.read()
                if expect_json and raw:
                    try:
                        return status, resp_headers, json.loads(raw)
                    except ValueError:
                        return status, resp_headers, raw
                return status, resp_headers, raw
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", "replace") if exc.fp else ""
            if exc.code in _RETRY_STATUSES and attempt <= _MAX_RETRIES:
                _backoff(attempt, exc)
                continue
            raise _safe_error(exc.code, raw, exc)
        except urllib.error.URLError as exc:
            if attempt <= _MAX_RETRIES:
                _backoff(attempt, None)
                continue
            raise LinkedInHTTPError(0, f"network error: {exc.reason}")


def _backoff(attempt, exc):
    """Sleep before a retry, honoring Retry-After when present."""
    delay = min(2 ** attempt, 30)
    if exc is not None and hasattr(exc, "headers") and exc.headers:
        retry_after = exc.headers.get("Retry-After")
        if retry_after and retry_after.isdigit():
            delay = min(int(retry_after), 60)
    time.sleep(delay)

"""OAuth token handling for the LinkedIn publisher.

LinkedIn access tokens last 60 days. Programmatic refresh tokens are gated to
approved partners, so this module is built to work either way:

  * If a refresh token + client id/secret are present, refresh on demand.
  * Otherwise use LINKEDIN_ACCESS_TOKEN directly and, when it is rejected,
    fail loudly with instructions to regenerate one.

Stdlib only.
"""

from __future__ import annotations

import datetime
import json
import urllib.error
import urllib.parse
import urllib.request

import ledger
from config import OAUTH_TOKEN_URL, TOKEN_GENERATOR_URL
from net import LinkedInHTTPError, linkedin_headers, request

_REGEN = (
    "No usable LinkedIn access token. Set LINKEDIN_ACCESS_TOKEN (and optionally "
    "LINKEDIN_REFRESH_TOKEN + LINKEDIN_CLIENT_ID + LINKEDIN_CLIENT_SECRET). "
    f"Generate a 60-day token at {TOKEN_GENERATOR_URL} with scopes "
    "w_organization_social r_organization_social, authorized by a page admin."
)


def refresh(cfg):
    """Exchange the refresh token for a fresh access token.

    Returns the token response dict. Records the derived expiry in the ledger.
    Raises RuntimeError with a non-secret message on failure.
    """
    if not cfg.has_refresh_creds():
        raise RuntimeError(
            "Cannot refresh: LINKEDIN_REFRESH_TOKEN, LINKEDIN_CLIENT_ID and "
            "LINKEDIN_CLIENT_SECRET must all be set. Programmatic refresh is "
            "available only to approved LinkedIn partners; if it is not enabled "
            f"for this app, regenerate a token at {TOKEN_GENERATOR_URL}."
        )
    payload = urllib.parse.urlencode({
        "grant_type": "refresh_token",
        "refresh_token": cfg.refresh_token,
        "client_id": cfg.client_id,
        "client_secret": cfg.client_secret,
    }).encode("utf-8")
    req = urllib.request.Request(
        OAUTH_TOKEN_URL, data=payload, method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace") if exc.fp else ""
        hint = ""
        try:
            hint = json.loads(raw).get("error_description", "")
        except ValueError:
            hint = raw[:200]
        raise RuntimeError(f"Token refresh failed (HTTP {exc.code}): {hint}")
    expires_in = int(data.get("expires_in", 0))
    if expires_in:
        expires_at = _utcnow() + datetime.timedelta(seconds=expires_in)
        ledger.set_token_expiry(cfg, expires_at.strftime("%Y-%m-%dT%H:%M:%SZ"))
    return data


def resolve_token(cfg, *, allow_refresh=True, verbose=False):
    """Return a usable access token string.

    Prefers a fresh token via refresh when refresh creds are present; falls back
    to the static access token; raises RuntimeError when neither works.
    """
    if allow_refresh and cfg.has_refresh_creds():
        try:
            data = refresh(cfg)
            if verbose:
                print("auth: refreshed access token")
            return data["access_token"]
        except RuntimeError as exc:
            if cfg.access_token:
                if verbose:
                    print(f"auth: refresh failed ({exc}); using static token")
                return cfg.access_token
            raise
    if cfg.access_token:
        return cfg.access_token
    raise RuntimeError(_REGEN)


def check(cfg, *, warn_days=7, verbose=False):
    """Validate the token with a cheap authenticated call and report expiry.

    Returns 0 when the token works and is not near expiry, 1 otherwise. Used by
    the token-health workflow to open a reminder issue before the 60-day expiry.
    """
    try:
        token = resolve_token(cfg, verbose=verbose)
    except RuntimeError as exc:
        print(f"check-token: FAIL — {exc}")
        return 1

    author = urllib.parse.quote(cfg.org_urn, safe="")
    url = f"{cfg.rest_base}/posts?author={author}&q=author&count=1"
    headers = linkedin_headers(token, cfg.api_version,
                               extra={"X-RestLi-Method": "FINDER"})
    try:
        request("GET", url, headers=headers)
    except LinkedInHTTPError as exc:
        if exc.status == 401:
            print(f"check-token: FAIL — token invalid or expired (HTTP 401). {_REGEN}")
            return 1
        if exc.status == 403:
            print("check-token: token authenticates but was DENIED reading the organization's "
                  "posts (HTTP 403). Likely causes: the token lacks r_organization_social (this "
                  "health check reads — posting needs w_organization_social, which may still work), "
                  "or the member is not an admin of the org. Regenerate with BOTH "
                  "w_organization_social and r_organization_social to make reads work.")
            return 1
        # Other errors (rate limit, transient) don't mean the token is dead.
        print(f"check-token: token accepted; API returned HTTP {exc.status}: {exc}")

    expires_at = ledger.get_token_expiry(cfg)
    if expires_at:
        try:
            exp = datetime.datetime.strptime(expires_at, "%Y-%m-%dT%H:%M:%SZ")
            days = (exp - _utcnow()).days
            print(f"check-token: token valid; ~{days} day(s) until expiry ({expires_at}).")
            if days <= warn_days:
                print(f"check-token: WARN — token expires within {warn_days} days. "
                      f"Regenerate at {TOKEN_GENERATOR_URL} or run `refresh-token`.")
                return 1
            return 0
        except ValueError:
            pass
    print("check-token: token valid. (No recorded expiry — access tokens last "
          "60 days from generation; run `refresh-token` to record one.)")
    return 0


def _utcnow():
    # datetime.utcnow() is deprecated in 3.12; use timezone-aware then drop tz
    # so the stored/compared strings stay naive-UTC and format-stable.
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

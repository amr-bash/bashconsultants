"""Configuration for the LinkedIn publisher.

Settings resolve with precedence: explicit override > environment variable >
built-in default. Secrets (tokens, client secret) come ONLY from the
environment — never a file the repo tracks. Non-secret values (the org URN, the
canonical host, the API version) have safe built-in defaults so `--dry-run`
works with no environment at all.

Stdlib only, matching scripts/content_lint.py.
"""

from __future__ import annotations

import os
from pathlib import Path

# scripts/features/linkedin/config.py -> parents: [linkedin, features, scripts, <repo root>]
REPO_ROOT = Path(__file__).resolve().parents[3]

# --- LinkedIn endpoints (stable) -------------------------------------------
REST_BASE = "https://api.linkedin.com/rest"
OAUTH_TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
TOKEN_GENERATOR_URL = "https://www.linkedin.com/developers/tools/oauth/token-generator"
RESTLI_VERSION = "2.0.0"

# --- Non-secret defaults (also mirrored in _config.yml `linkedin:`) ---------
DEFAULT_ORG_URN = "urn:li:organization:64517157"
DEFAULT_BASE_URL = "https://bash-365.com"
DEFAULT_API_VERSION = "202606"  # LinkedIn-Version, YYYYMM; bump ~yearly

# --- Repo paths -------------------------------------------------------------
LEDGER_PATH = REPO_ROOT / ".github" / "linkedin-log.json"
QUEUE_DIR = REPO_ROOT / "drafts" / "linkedin"
PREVIEWS_DIR = REPO_ROOT / "assets" / "images" / "previews"
POSTS_GLOB = "pages/_posts/**/*.md"
# jekyll-seo-tag site-wide image fallback (see _config.yml `og_image`)
FALLBACK_IMAGE = REPO_ROOT / "assets" / "images" / "office.jpg"

COMMENTARY_MAX = 3000  # LinkedIn hard limit on post commentary


class Config:
    """Resolved runtime settings. Overrides win, then env, then defaults."""

    def __init__(self, *, base_url=None, org_urn=None, api_version=None):
        self.org_urn = org_urn or os.environ.get("LINKEDIN_ORG_URN") or DEFAULT_ORG_URN
        self.base_url = (
            base_url or os.environ.get("LINKEDIN_BASE_URL") or DEFAULT_BASE_URL
        ).rstrip("/")
        self.api_version = (
            api_version or os.environ.get("LINKEDIN_API_VERSION") or DEFAULT_API_VERSION
        )
        # Secrets — never defaulted, never logged.
        self.access_token = os.environ.get("LINKEDIN_ACCESS_TOKEN") or ""
        self.refresh_token = os.environ.get("LINKEDIN_REFRESH_TOKEN") or ""
        self.client_id = os.environ.get("LINKEDIN_CLIENT_ID") or ""
        self.client_secret = os.environ.get("LINKEDIN_CLIENT_SECRET") or ""

    @property
    def rest_base(self) -> str:
        return REST_BASE

    def has_refresh_creds(self) -> bool:
        return bool(self.refresh_token and self.client_id and self.client_secret)

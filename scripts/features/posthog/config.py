"""Configuration for the PostHog server-side tool.

The personal API key (POSTHOG_API_KEY, prefix `phx_`) is a SECRET and comes only
from the environment (.env locally, Actions secrets in CI). Non-secret values —
the project id, region, and the public client key the site ships — are read from
_config.yml's `posthog:` block so there is one source of truth, with env
overrides. Stdlib only, matching scripts/content_lint.py.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
CONFIG_YML = REPO_ROOT / "_config.yml"

REGION_HOSTS = {"us": "https://us.posthog.com", "eu": "https://eu.posthog.com"}


def _scan_config_yml():
    """Extract posthog.{api_key, project_id, api_region} without a YAML lib."""
    vals = {}
    if not CONFIG_YML.exists():
        return vals
    text = CONFIG_YML.read_text(encoding="utf-8")
    m = re.search(r"^\s*api_key\s*:\s*'(phc_[A-Za-z0-9]+)'", text, re.M)
    if m:
        vals["client_key"] = m.group(1)
    m = re.search(r"^\s*project_id\s*:\s*(\d+)", text, re.M)
    if m:
        vals["project_id"] = m.group(1)
    m = re.search(r"^\s*api_region\s*:\s*'?([a-z]{2})'?", text, re.M)
    if m:
        vals["region"] = m.group(1)
    return vals


class Config:
    def __init__(self, *, project_id=None, region=None):
        cfg = _scan_config_yml()
        self.personal_key = os.environ.get("POSTHOG_API_KEY", "")
        self.project_id = str(
            project_id or os.environ.get("POSTHOG_PROJECT_ID") or cfg.get("project_id") or "")
        self.region = (region or os.environ.get("POSTHOG_API_REGION")
                       or cfg.get("region") or "us")
        # The public client (write) key the site actually ships, for drift checks.
        self.client_key = os.environ.get("POSTHOG_PROJECT_KEY") or cfg.get("client_key") or ""

    @property
    def api_base(self):
        return REGION_HOSTS.get(self.region, REGION_HOSTS["us"])

    def require(self):
        if not self.personal_key:
            raise RuntimeError(
                "POSTHOG_API_KEY is not set. Add your PostHog personal API key "
                "(prefix phx_) to .env locally or the Actions secret. Create one at "
                "https://us.posthog.com/settings/user-api-keys")
        if not self.project_id:
            raise RuntimeError(
                "No PostHog project id. Set posthog.project_id in _config.yml or "
                "POSTHOG_PROJECT_ID in the environment.")

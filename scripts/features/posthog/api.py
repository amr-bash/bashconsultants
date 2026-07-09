"""Thin wrappers over the PostHog project REST API."""

from __future__ import annotations

import urllib.parse

from net import request

# Privacy-relevant project fields this tool reads and reports on.
SETTINGS_FIELDS = [
    "name",
    "api_token",
    "anonymize_ips",
    "session_recording_opt_in",
    "capture_console_log_opt_in",
    "capture_performance_opt_in",
    "autocapture_opt_out",
    "event_retention_months",
    "events_retention_enforced",
    "ingested_event",
]


def get_project(cfg):
    url = f"{cfg.api_base}/api/projects/{cfg.project_id}/"
    _, _, body = request("GET", url, cfg.personal_key)
    return body


def patch_project(cfg, changes):
    url = f"{cfg.api_base}/api/projects/{cfg.project_id}/"
    _, _, body = request("PATCH", url, cfg.personal_key, json_body=changes)
    return body


def create_annotation(cfg, content, *, date_marker=None):
    url = f"{cfg.api_base}/api/projects/{cfg.project_id}/annotations/"
    payload = {"content": content, "scope": "project"}
    if date_marker:
        payload["date_marker"] = date_marker
    _, _, body = request("POST", url, cfg.personal_key, json_body=payload)
    return body


def project_url(cfg):
    return f"{cfg.api_base}/project/{cfg.project_id}"

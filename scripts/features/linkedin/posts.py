"""Build and send posts to the LinkedIn Posts API (`/rest/posts`).

Two envelopes: a plain text update and an article (link) share. LinkedIn does
not scrape the URL, so an article share carries its own title, description and
thumbnail URN. A successful create returns 201 with the post URN in the
`x-restli-id` response header.

Stdlib only.
"""

from __future__ import annotations

import urllib.parse

from net import request, linkedin_headers

_DISTRIBUTION = {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": [],
}


def build_text_payload(cfg, commentary):
    return {
        "author": cfg.org_urn,
        "commentary": commentary,
        "visibility": "PUBLIC",
        "distribution": _DISTRIBUTION,
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }


def build_article_payload(cfg, *, url, title, description, commentary,
                          thumbnail_urn=None):
    article = {"source": url, "title": title, "description": description}
    if thumbnail_urn:
        article["thumbnail"] = thumbnail_urn
    payload = build_text_payload(cfg, commentary)
    payload["content"] = {"article": article}
    return payload


def create_post(cfg, token, payload):
    """POST a payload and return the created post URN (from x-restli-id)."""
    url = f"{cfg.rest_base}/posts"
    status, headers, _ = request(
        "POST", url,
        headers=linkedin_headers(token, cfg.api_version),
        json_body=payload,
    )
    # Header names are case-insensitive in the response dict we built; check both.
    urn = headers.get("x-restli-id") or headers.get("X-RestLi-Id")
    if not urn:
        for key, value in headers.items():
            if key.lower() == "x-restli-id":
                urn = value
                break
    if not urn:
        raise RuntimeError(f"post created (HTTP {status}) but no x-restli-id header returned")
    return urn


def get_post(cfg, token, urn):
    """Fetch a post by URN (needs r_organization_social)."""
    encoded = urllib.parse.quote(urn, safe="")
    url = f"{cfg.rest_base}/posts/{encoded}"
    _, _, data = request("GET", url,
                         headers=linkedin_headers(token, cfg.api_version))
    return data


def feed_url(urn):
    """The public permalink for a published post."""
    return f"https://www.linkedin.com/feed/update/{urn}/"

"""Image upload for article-share thumbnails (LinkedIn Images API).

Three steps: initializeUpload -> PUT the bytes to the returned signed URL ->
(optionally) poll until the asset is AVAILABLE. Returns an `urn:li:image:...`
to drop into a post's `content.article.thumbnail`.

The thumbnail is optional on a post, so callers can treat any failure here as a
warning and post without an image.

Stdlib only.
"""

from __future__ import annotations

import time
import urllib.parse
from pathlib import Path

from net import request, linkedin_headers

_CONTENT_TYPES = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def upload_image(cfg, token, image_path, *, verbose=False):
    """Upload a local image file and return its image URN."""
    path = Path(image_path)
    raw = path.read_bytes()

    # 1. initializeUpload — register the asset, get a signed upload URL + URN.
    init_url = f"{cfg.rest_base}/images?action=initializeUpload"
    body = {"initializeUploadRequest": {"owner": cfg.org_urn}}
    _, _, data = request("POST", init_url,
                         headers=linkedin_headers(token, cfg.api_version),
                         json_body=body)
    value = data.get("value") or {}
    upload_url = value.get("uploadUrl")
    image_urn = value.get("image")
    if not upload_url or not image_urn:
        raise RuntimeError("initializeUpload returned no uploadUrl/image URN")
    if verbose:
        print(f"images: uploading {path.name} ({len(raw)} bytes) -> {image_urn}")

    # 2. PUT the bytes to the signed URL (bearer auth required).
    content_type = _CONTENT_TYPES.get(path.suffix.lower(), "application/octet-stream")
    put_headers = {"Authorization": f"Bearer {token}", "Content-Type": content_type}
    request("PUT", upload_url, headers=put_headers, raw_body=raw, expect_json=False)

    # 3. Best-effort: wait until the asset is processed. The URN is usable for
    #    an article thumbnail even mid-processing, so never block on this.
    _wait_available(cfg, token, image_urn, verbose=verbose)
    return image_urn


def _wait_available(cfg, token, image_urn, *, attempts=4, delay=2, verbose=False):
    encoded = urllib.parse.quote(image_urn, safe="")
    url = f"{cfg.rest_base}/images/{encoded}"
    for _ in range(attempts):
        try:
            _, _, data = request("GET", url,
                                 headers=linkedin_headers(token, cfg.api_version))
        except Exception:
            return  # never block the post on a status probe
        status = (data or {}).get("status")
        if status in (None, "AVAILABLE"):
            return
        if verbose:
            print(f"images: {image_urn} status={status}; waiting…")
        time.sleep(delay)

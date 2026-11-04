"""Moped-specific safe endpoint configuration.

Blocket exposes moped class filters on the public scooter search page.
Its dedicated JSON endpoint SEARCH_ID_MC_SCOOTER was verified against
real class I and II searches on 2026-11-04.
"""
from __future__ import annotations

import os
from urllib.parse import urlsplit

from .constants import MOPED_SEARCH_URL


def resolve_moped_search_url(explicit_url: str | None = None) -> str:
    """Return Blocket's verified moped JSON endpoint or an explicit override.

    To prevent passing an arbitrary host through the client, only HTTPS
    Blocket search API URLs are accepted. URLs with queries/fragments or
    userinfo are rejected; filters are always sent as separate params.
    """
    url = explicit_url or os.environ.get("BLOCKET_MOPED_SEARCH_URL") or MOPED_SEARCH_URL
    parsed = urlsplit(url)
    if (
        parsed.scheme != "https"
        or parsed.netloc != "www.blocket.se"
        or not parsed.path.startswith("/mobility/search/api/search/SEARCH_ID_")
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("moped_search_url must be a Blocket HTTPS mobility JSON search endpoint")
    return url

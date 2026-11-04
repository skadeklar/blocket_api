"""Moped-specific safe endpoint configuration.

Blocket exposes moped class filters on the public scooter search page.
A corresponding JSON endpoint has not yet been independently verified.
No guessed search ID is used: the endpoint must be explicitly configured.
"""
from __future__ import annotations

import os
from urllib.parse import urlsplit


def resolve_moped_search_url(explicit_url: str | None = None) -> str:
    """Return the verified JSON search endpoint configured by the caller.

    To prevent passing an arbitrary host through the client, only HTTPS
    Blocket search API URLs are accepted. URLs with queries/fragments or
    userinfo are rejected; filters are always sent as separate params.
    """
    url = explicit_url or os.environ.get("BLOCKET_MOPED_SEARCH_URL")
    if not url:
        raise RuntimeError(
            "Moped search is not configured: verify the JSON endpoint used by "
            "https://www.blocket.se/mobility/search/mc/scooter and set "
            "BLOCKET_MOPED_SEARCH_URL server-side or pass moped_search_url=."
        )
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

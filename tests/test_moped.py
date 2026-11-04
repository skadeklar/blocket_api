"""Offline tests for Skadeklar's moped search extension.

These tests deliberately do not access Blocket; a live search endpoint
has separately been verified with live class-I/II listings.
"""
from typing import Any

import httpx
import pytest

from blocket_api import AsyncBlocketAPI, BlocketAPI, McModel, MopedType
from blocket_api._params import build_moped_params
from blocket_api.constants import MOPED_SEARCH_URL
from blocket_api.moped import resolve_moped_search_url


TEST_URL = (
    "https://www.blocket.se/mobility/search/api/search/"
    "SEARCH_ID_TEST_MOPED"
)


def test_moped_params_include_both_classes_and_no_mopedcar() -> None:
    params = build_moped_params("Speedfight", models=[McModel.PEUGEOT])
    assert ("q", "Speedfight") in params
    assert ("make", McModel.PEUGEOT.value) in params
    assert [value for name, value in params if name == "type"] == [6, 8]
    assert 10 not in [value for name, value in params if name == "type"]


def test_moped_params_selected_type() -> None:
    params = build_moped_params("Viarelli", types=[MopedType.KLASS_II])
    assert [value for name, value in params if name == "type"] == [8]


@pytest.mark.parametrize("kwargs", [
    {"types": []},
    {"page": 0},
    {"price_from": -5},
    {"mileage_to": -1},
])
def test_invalid_filters_raise(kwargs: dict[str, Any]) -> None:
    with pytest.raises(ValueError):
        build_moped_params(**kwargs)


def test_moped_url_must_be_verified_and_configured(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("BLOCKET_MOPED_SEARCH_URL", raising=False)
    assert resolve_moped_search_url() == MOPED_SEARCH_URL
    for unsafe in (
        "https://example.com/mobility/search/api/search/SEARCH_ID_X",
        "http://www.blocket.se/mobility/search/api/search/SEARCH_ID_X",
        "https://www.blocket.se/mobility/search/mc/scooter",
        TEST_URL + "?q=abc",
    ):
        with pytest.raises(ValueError):
            resolve_moped_search_url(unsafe)


def test_sync_moped_search_reuses_current_httpx(monkeypatch: pytest.MonkeyPatch) -> None:
    observed: dict[str, Any] = {}

    def get(url: str, *, headers: dict[str, str], params: list[tuple[str, Any]]) -> httpx.Response:
        observed["url"] = url
        observed["params"] = params
        return httpx.Response(200, json={"docs": [{"heading": "Peugeot"}]},
                              request=httpx.Request("GET", url))

    monkeypatch.setattr(httpx, "get", get)
    out = BlocketAPI(moped_search_url=TEST_URL).search_moped(
        "Speedfight", price_to=20000, models=[McModel.PEUGEOT]
    )
    assert out["docs"][0]["heading"] == "Peugeot"
    assert observed["url"] == TEST_URL
    assert ("price_to", 20000) in observed["params"]
    assert [v for k, v in observed["params"] if k == "type"] == [6, 8]


@pytest.mark.asyncio
async def test_async_moped_search_uses_configured_endpoint() -> None:
    calls: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return httpx.Response(200, json={"docs": []}, request=request)

    async with httpx.AsyncClient(transport=httpx.MockTransport(handler)) as client:
        api = AsyncBlocketAPI(client, moped_search_url=TEST_URL)
        result = await api.search_moped(
            "Rieju", types=[MopedType.EU_KLASS_I]
        )
    assert result == {"docs": []}
    assert len(calls) == 1
    assert str(calls[0].url).startswith(TEST_URL)
    assert calls[0].url.params.get_list("type") == ["6"]

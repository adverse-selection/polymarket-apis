from __future__ import annotations

from unittest.mock import Mock

from polymarket_apis.clients.gamma_client import PolymarketGammaClient


def test_get_markets_passes_include_tag_query_param() -> None:
    client = PolymarketGammaClient()
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = [{"id": "1"}]
    client.client = Mock()
    client.client.get.return_value = response

    client.get_markets(limit=1, include_tag=True)

    _, kwargs = client.client.get.call_args
    assert kwargs["params"]["include_tag"] is True

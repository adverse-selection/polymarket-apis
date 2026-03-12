from __future__ import annotations

from datetime import UTC, datetime
from unittest.mock import Mock

from polymarket_apis.clients.clob_client import PolymarketReadOnlyClobClient


def test_get_order_book_history_converts_datetime_range_to_unix_seconds() -> None:
    client = PolymarketReadOnlyClobClient()
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"count": 0, "data": []}
    client.client = Mock()
    client.client.get.return_value = response

    start_time = datetime(2026, 2, 21, 7, 15, 0, 900_000, tzinfo=UTC)
    end_time = datetime(2026, 2, 21, 8, 15, 0, 100_000, tzinfo=UTC)

    client.get_order_book_history(
        asset_id="9306951013082032190893794706797543486571692644330379641891856482591227807119",
        start_time=start_time,
        end_time=end_time,
    )

    _, kwargs = client.client.get.call_args
    assert kwargs["params"] == {
        "asset_id": "9306951013082032190893794706797543486571692644330379641891856482591227807119",
        "startTs": 1771658100,
        "endTs": 1771661700,
    }


def test_get_order_book_history_parses_response() -> None:
    client = PolymarketReadOnlyClobClient()
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "count": 1,
        "data": [
            {
                "market": "0x86dbf1cff391c05a0fa3ac841e8c63b22689a9c9aa2267c641187cacb6092c74",
                "asset_id": "9306951013082032190893794706797543486571692644330379641891856482591227807119",
                "timestamp": "1771557804187",
                "hash": "4dbf4ab85efb236e327370eb92a641a253143bf9",
                "bids": [{"price": "0.01", "size": "3829"}],
                "asks": [{"price": "0.99", "size": "3829"}],
                "min_order_size": "5",
                "tick_size": "0.01",
                "neg_risk": False,
                "last_trade_price": "",
            }
        ],
    }
    client.client = Mock()
    client.client.get.return_value = response

    parsed = client.get_order_book_history(
        asset_id="9306951013082032190893794706797543486571692644330379641891856482591227807119",
        start_time=datetime.fromtimestamp(1771643700, tz=UTC),
    )

    assert parsed.count == 1
    assert (
        parsed.data[0].token_id
        == "9306951013082032190893794706797543486571692644330379641891856482591227807119"
    )
    assert parsed.data[0].last_trade_price is None


def test_get_order_book_history_omits_end_ts_when_not_provided() -> None:
    client = PolymarketReadOnlyClobClient()
    response = Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"count": 0, "data": []}
    client.client = Mock()
    client.client.get.return_value = response

    client.get_order_book_history(
        asset_id="9306951013082032190893794706797543486571692644330379641891856482591227807119",
        start_time=datetime.fromtimestamp(1771643700, tz=UTC),
    )

    _, kwargs = client.client.get.call_args
    assert kwargs["params"] == {
        "asset_id": "9306951013082032190893794706797543486571692644330379641891856482591227807119",
        "startTs": 1771643700,
    }

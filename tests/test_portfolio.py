import pytest
from utils.storage import (
    load_portfolio,
    save_portfolio,
    load_pinned_stocks,
    save_pinned_stocks,
    add_position,
    delete_position,
    pin_stock,
    unpin_stock,
)


class TestStorage:
    def test_save_and_load_portfolio(self):
        positions = [
            {"symbol": "AAPL", "quantity": 10, "purchase_price": 150},
        ]

        save_portfolio(positions)
        loaded = load_portfolio()

        assert len(loaded) >= 1
        assert loaded[0]["symbol"] == "AAPL"

    def test_add_position(self):
        initial = load_portfolio()
        initial_count = len(initial)

        position = {
            "symbol": "MSFT",
            "quantity": 5,
            "purchase_price": 300,
        }

        add_position(position)
        updated = load_portfolio()

        assert len(updated) == initial_count + 1

    def test_delete_position(self):
        positions = load_portfolio()

        if positions:
            pos_id = positions[0].get("id")
            if pos_id:
                delete_position(pos_id)
                updated = load_portfolio()
                assert pos_id not in [p.get("id") for p in updated]

    def test_save_and_load_pinned(self):
        test_symbols = ["AAPL", "MSFT", "GOOGL"]

        save_pinned_stocks(test_symbols)
        loaded = load_pinned_stocks()

        assert loaded == test_symbols

    def test_pin_stock(self):
        initial = load_pinned_stocks()
        initial_len = len(initial)

        pin_stock("NVDA")
        updated = load_pinned_stocks()

        assert "NVDA" in updated
        assert len(updated) == initial_len + 1

    def test_unpin_stock(self):
        save_pinned_stocks(["AAPL", "MSFT"])

        unpin_stock("AAPL")
        updated = load_pinned_stocks()

        assert "AAPL" not in updated
        assert "MSFT" in updated

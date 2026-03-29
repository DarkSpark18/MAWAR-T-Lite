import pytest
from modules.data_fetcher import (
    validate_ticker_exists,
    get_returns_data,
)


class TestDataFetcher:
    def test_validate_ticker_invalid(self):
        result = validate_ticker_exists("INVALIDTICKER123XYZ")
        assert result == False

    def test_get_returns_data_returns_tuple(self):
        mean, vol = get_returns_data("AAPL", days=30)
        assert isinstance(mean, float)
        assert isinstance(vol, float)

    def test_get_returns_data_invalid_ticker(self):
        mean, vol = get_returns_data("INVALIDTICKER123", days=10)
        assert mean == 0.0
        assert vol == 0.0

import pytest
from utils.validators import (
    validate_ticker,
    validate_price,
    validate_quantity,
    validate_date,
    validate_confidence,
    validate_simulation_count,
    validate_prediction_days,
    sanitize_ticker,
    validate_portfolio_position,
)


class TestValidators:
    def test_validate_ticker_valid(self):
        assert validate_ticker("AAPL") == True
        assert validate_ticker("MSFT") == True
        assert validate_ticker("BRK.B") == True
        assert validate_ticker("aapl") == True

    def test_validate_ticker_invalid(self):
        assert validate_ticker("") == False
        assert validate_ticker("TOOLONG") == False
        assert validate_ticker("123") == False
        assert validate_ticker("AAPL-B") == False

    def test_validate_price_valid(self):
        assert validate_price(100) == True
        assert validate_price(0.01) == True
        assert validate_price(1000.50) == True

    def test_validate_price_invalid(self):
        assert validate_price(0) == False
        assert validate_price(-10) == False
        assert validate_price("abc") == False

    def test_validate_quantity_valid(self):
        assert validate_quantity(10) == True
        assert validate_quantity(0.5) == True
        assert validate_quantity(1000) == True

    def test_validate_quantity_invalid(self):
        assert validate_quantity(0) == False
        assert validate_quantity(-5) == False
        assert validate_quantity("ten") == False

    def test_validate_date_valid(self):
        assert validate_date("2024-01-15") == True
        assert validate_date("2023-12-31") == True

    def test_validate_date_invalid(self):
        assert validate_date("2024/01/15") == False
        assert validate_date("01-15-2024") == False
        assert validate_date("invalid") == False
        assert validate_date(None) == False

    def test_validate_confidence(self):
        assert validate_confidence(68) == True
        assert validate_confidence(95) == True
        assert validate_confidence(99) == True
        assert validate_confidence(90) == False

    def test_validate_simulation_count(self):
        assert validate_simulation_count(100) == True
        assert validate_simulation_count(5000) == True
        assert validate_simulation_count(10000) == True
        assert validate_simulation_count(50) == False
        assert validate_simulation_count(20000) == False

    def test_validate_prediction_days(self):
        assert validate_prediction_days(30) == True
        assert validate_prediction_days(60) == True
        assert validate_prediction_days(90) == True
        assert validate_prediction_days(180) == True
        assert validate_prediction_days(365) == True
        assert validate_prediction_days(45) == False

    def test_sanitize_ticker(self):
        assert sanitize_ticker("aapl") == "AAPL"
        assert sanitize_ticker(" msft ") == "MSFT"
        assert sanitize_ticker("") == ""

    def test_validate_portfolio_position_valid(self):
        position = {
            "symbol": "AAPL",
            "quantity": 10,
            "purchase_price": 150.0,
            "purchase_date": "2024-01-15",
        }

        is_valid, error = validate_portfolio_position(position)

        assert is_valid == True
        assert error is None

    def test_validate_portfolio_position_invalid(self):
        position = {}

        is_valid, error = validate_portfolio_position(position)

        assert is_valid == False
        assert "symbol" in error.lower()

    def test_validate_portfolio_position_bad_symbol(self):
        position = {
            "symbol": "INVALIDTICKER",
            "quantity": 10,
            "purchase_price": 150.0,
        }

        is_valid, error = validate_portfolio_position(position)

        assert is_valid == False
        assert "ticker" in error.lower()

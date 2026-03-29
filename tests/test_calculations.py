import pytest
import numpy as np
from utils.calculations import (
    calculate_returns,
    calculate_mean_return,
    calculate_volatility,
    calculate_portfolio_value,
    calculate_portfolio_cost,
    calculate_position_pnl,
    calculate_total_pnl,
    format_currency,
    format_percentage,
    monte_carlo_simulation,
    get_confidence_intervals,
)


class TestCalculations:
    def test_calculate_returns(self):
        prices = np.array([100, 105, 102, 108, 110])
        returns = calculate_returns(prices)

        assert len(returns) == len(prices) - 1
        assert returns[0] == pytest.approx(0.05)

    def test_calculate_mean_return(self):
        prices = np.array([100, 105, 102, 108, 110])
        mean_ret = calculate_mean_return(prices)

        assert isinstance(mean_ret, float)

    def test_calculate_volatility(self):
        prices = np.array([100, 105, 102, 108, 110])
        vol = calculate_volatility(prices)

        assert vol >= 0

    def test_calculate_portfolio_value(self):
        positions = [
            {"symbol": "AAPL", "quantity": 10},
            {"symbol": "MSFT", "quantity": 5},
        ]
        prices = {"AAPL": 150.0, "MSFT": 300.0}

        value = calculate_portfolio_value(positions, prices)

        assert value == 10 * 150 + 5 * 300
        assert value == 3000.0

    def test_calculate_portfolio_cost(self):
        positions = [
            {"symbol": "AAPL", "quantity": 10, "purchase_price": 140},
            {"symbol": "MSFT", "quantity": 5, "purchase_price": 280},
        ]

        cost = calculate_portfolio_cost(positions)

        assert cost == 10 * 140 + 5 * 280
        assert cost == 2800.0

    def test_calculate_position_pnl(self):
        position = {"quantity": 10, "purchase_price": 100}
        current_price = 120

        pnl = calculate_position_pnl(position, current_price)

        assert pnl["current_value"] == 1200
        assert pnl["cost_basis"] == 1000
        assert pnl["pnl"] == 200
        assert pnl["pnl_pct"] == 20.0

    def test_calculate_total_pnl(self):
        positions = [
            {"symbol": "AAPL", "quantity": 10, "purchase_price": 100},
        ]
        prices = {"AAPL": 120}

        pnl = calculate_total_pnl(positions, prices)

        assert pnl["total_value"] == 1200
        assert pnl["total_cost"] == 1000
        assert pnl["pnl"] == 200

    def test_format_currency(self):
        assert format_currency(1234.56) == "$1,234.56"
        assert format_currency(0) == "$0.00"
        assert format_currency(1000000) == "$1,000,000.00"

    def test_format_percentage(self):
        assert format_percentage(5.5) == "+5.50%"
        assert format_percentage(-3.2) == "-3.20%"
        assert format_percentage(0) == "0.00%"

    def test_monte_carlo_simulation(self):
        price_paths, final_prices = monte_carlo_simulation(
            initial_price=100,
            days=30,
            simulations=100,
            volatility=0.02,
            mean_return=0.0005,
        )

        assert price_paths.shape == (100, 31)
        assert len(final_prices) == 100
        assert final_prices[0] > 0

    def test_get_confidence_intervals(self):
        prices = np.random.normal(100, 10, 1000)
        lower, median, upper = get_confidence_intervals(prices, 0.95)

        assert lower < median < upper
        assert 0 < lower < 150
        assert 50 < upper < 150

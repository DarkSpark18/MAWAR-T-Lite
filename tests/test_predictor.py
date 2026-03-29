import pytest
from modules.predictor import (
    stock_selection_ui,
    simulation_parameters_ui,
    run_monte_carlo,
)


class TestPredictor:
    def test_run_monte_carlo_shape(self):
        import numpy as np

        price_paths, final_prices = run_monte_carlo(
            initial_price=100.0,
            mean_return=0.0005,
            volatility=0.02,
            days=30,
            simulations=100,
        )

        assert price_paths.shape == (100, 31)
        assert len(final_prices) == 100

    def test_run_monte_carlo_prices_positive(self):
        import numpy as np

        price_paths, final_prices = run_monte_carlo(
            initial_price=100.0,
            mean_return=0.0,
            volatility=0.02,
            days=30,
            simulations=50,
        )

        assert np.all(price_paths > 0)
        assert np.all(final_prices > 0)

    def test_run_monte_carlo_zero_volatility(self):
        import numpy as np

        price_paths, final_prices = run_monte_carlo(
            initial_price=100.0,
            mean_return=0.0,
            volatility=0.0,
            days=30,
            simulations=10,
        )

        assert np.allclose(price_paths, 100.0)
        assert np.allclose(final_prices, 100.0)

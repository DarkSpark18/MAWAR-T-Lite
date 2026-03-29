import numpy as np
from typing import Dict, List, Tuple


def calculate_returns(prices: np.ndarray) -> np.ndarray:
    return np.diff(prices) / prices[:-1]


def calculate_mean_return(prices: np.ndarray) -> float:
    returns = calculate_returns(prices)
    return float(np.mean(returns))


def calculate_volatility(prices: np.ndarray) -> float:
    returns = calculate_returns(prices)
    return float(np.std(returns))


def calculate_portfolio_value(
    positions: List[Dict], current_prices: Dict[str, float]
) -> float:
    total = 0.0
    for pos in positions:
        symbol = pos.get("symbol", "").upper()
        quantity = float(pos.get("quantity", 0))
        if symbol in current_prices:
            total += quantity * current_prices[symbol]
    return total


def calculate_portfolio_cost(positions: List[Dict]) -> float:
    total = 0.0
    for pos in positions:
        quantity = float(pos.get("quantity", 0))
        price = float(pos.get("purchase_price", 0))
        total += quantity * price
    return total


def calculate_position_pnl(position: Dict, current_price: float) -> Dict:
    quantity = float(position.get("quantity", 0))
    purchase_price = float(position.get("purchase_price", 0))
    current_value = quantity * current_price
    cost_basis = quantity * purchase_price
    pnl = current_value - cost_basis
    pnl_pct = (pnl / cost_basis * 100) if cost_basis > 0 else 0

    return {
        "current_value": current_value,
        "cost_basis": cost_basis,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
    }


def calculate_total_pnl(
    positions: List[Dict], current_prices: Dict[str, float]
) -> Dict:
    total_value = calculate_portfolio_value(positions, current_prices)
    total_cost = calculate_portfolio_cost(positions)
    pnl = total_value - total_cost
    pnl_pct = (pnl / total_cost * 100) if total_cost > 0 else 0

    return {
        "total_value": total_value,
        "total_cost": total_cost,
        "pnl": pnl,
        "pnl_pct": pnl_pct,
    }


def calculate_var(returns: np.ndarray, confidence: float = 0.95) -> float:
    confidence_level = int((1 - confidence) * len(returns))
    sorted_returns = np.sort(returns)
    return (
        float(np.abs(sorted_returns[confidence_level]))
        if confidence_level < len(sorted_returns)
        else 0.0
    )


def calculate_sharpe_ratio(returns: np.ndarray, risk_free_rate: float = 0.02) -> float:
    mean_return = np.mean(returns)
    std_return = np.std(returns)
    if std_return == 0:
        return 0.0
    return float((mean_return - risk_free_rate) / std_return)


def calculate_portfolio_allocation(
    positions: List[Dict], current_prices: Dict[str, float]
) -> Dict[str, float]:
    total_value = calculate_portfolio_value(positions, current_prices)
    if total_value == 0:
        return {}

    allocation = {}
    for pos in positions:
        symbol = pos.get("symbol", "").upper()
        quantity = float(pos.get("quantity", 0))
        if symbol in current_prices:
            value = quantity * current_prices[symbol]
            allocation[symbol] = (value / total_value) * 100

    return allocation


def monte_carlo_simulation(
    initial_price: float,
    days: int,
    simulations: int,
    volatility: float,
    mean_return: float,
) -> Tuple[np.ndarray, np.ndarray]:
    dt = 1 / 252
    drift = (mean_return - 0.5 * volatility**2) * dt
    diffusion = (
        volatility * np.sqrt(dt) * np.random.standard_normal((simulations, days))
    )

    price_paths = np.zeros((simulations, days + 1))
    price_paths[:, 0] = initial_price
    price_paths[:, 1:] = initial_price * np.exp(np.cumsum(drift + diffusion, axis=1))

    final_prices = price_paths[:, -1]

    return price_paths, final_prices


def get_confidence_intervals(
    prices: np.ndarray, confidence: float = 0.95
) -> Tuple[float, float, float]:
    lower = (1 - confidence) / 2
    upper = 1 - lower
    lower_val = np.percentile(prices, lower * 100)
    upper_val = np.percentile(prices, upper * 100)
    median = np.median(prices)
    return lower_val, median, upper_val


def format_currency(value: float, currency: str = "USD") -> str:
    symbols = {"USD": "$", "EUR": "€", "GBP": "£"}
    symbol = symbols.get(currency, "$")
    return f"{symbol}{value:,.2f}"


def format_percentage(value: float) -> str:
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.2f}%"

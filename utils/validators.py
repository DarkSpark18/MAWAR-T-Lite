import re
from datetime import datetime
from typing import Optional


def validate_ticker(ticker: str) -> bool:
    if not ticker or not isinstance(ticker, str):
        return False
    ticker = ticker.strip().upper()
    pattern = r"^[A-Z]{1,5}(\.[A-Z]{1,2})?$"
    return bool(re.match(pattern, ticker))


def validate_price(price: float) -> bool:
    return isinstance(price, (int, float)) and price > 0


def validate_quantity(quantity: float) -> bool:
    return isinstance(quantity, (int, float)) and quantity > 0


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except (ValueError, TypeError):
        return False


def validate_confidence(confidence: int) -> bool:
    return confidence in [68, 95, 99]


def validate_simulation_count(count: int) -> bool:
    return 100 <= count <= 10000


def validate_prediction_days(days: int) -> bool:
    return days in [30, 60, 90, 180, 365]


def sanitize_ticker(ticker: str) -> str:
    return ticker.strip().upper() if ticker else ""


def validate_portfolio_position(position: dict) -> tuple[bool, Optional[str]]:
    required_fields = ["symbol", "quantity", "purchase_price"]

    for field in required_fields:
        if field not in position:
            return False, f"Missing required field: {field}"

    if not validate_ticker(position["symbol"]):
        return False, "Invalid ticker symbol"

    if not validate_quantity(position["quantity"]):
        return False, "Invalid quantity"

    if not validate_price(position["purchase_price"]):
        return False, "Invalid purchase price"

    if "purchase_date" in position and not validate_date(position["purchase_date"]):
        return False, "Invalid date format (use YYYY-MM-DD)"

    return True, None

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)


def load_json(filename: str, default: Any = None) -> Any:
    filepath = os.path.join(DATA_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return json.load(f)
    return default if default is not None else {}


def save_json(filename: str, data: Any) -> None:
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2, default=str)


def load_portfolio() -> List[Dict]:
    positions = load_json("portfolio.json", [])
    for i, pos in enumerate(positions):
        if "id" not in pos:
            pos["id"] = str(datetime.now().timestamp()) + f"_{i}"
    return positions


def save_portfolio(positions: List[Dict]) -> None:
    save_json("portfolio.json", positions)


def load_pinned_stocks() -> List[str]:
    return load_json("pinned_stocks.json", [])


def save_pinned_stocks(symbols: List[str]) -> None:
    save_json("pinned_stocks.json", symbols)


def add_position(position: Dict) -> bool:
    positions = load_portfolio()
    position["id"] = str(datetime.now().timestamp())
    position["added_at"] = datetime.now().isoformat()
    positions.append(position)
    save_portfolio(positions)
    return True


def update_position(position_id: str, updates: Dict) -> bool:
    positions = load_portfolio()
    for i, pos in enumerate(positions):
        if pos.get("id") == position_id:
            positions[i].update(updates)
            positions[i]["updated_at"] = datetime.now().isoformat()
            save_portfolio(positions)
            return True
    return False


def delete_position(position_id: str) -> bool:
    positions = load_portfolio()
    positions = [p for p in positions if p.get("id") != position_id]
    save_portfolio(positions)
    return True


def pin_stock(symbol: str) -> bool:
    pinned = load_pinned_stocks()
    if len(pinned) >= 5:
        return False
    if symbol not in pinned:
        pinned.append(symbol)
        save_pinned_stocks(pinned)
    return True


def unpin_stock(symbol: str) -> bool:
    pinned = load_pinned_stocks()
    if symbol in pinned:
        pinned.remove(symbol)
        save_pinned_stocks(pinned)
    return True


def reorder_pinned_stocks(symbols: List[str]) -> None:
    save_pinned_stocks(symbols)


def export_to_csv(positions: List[Dict], filepath: str) -> bool:
    try:
        import csv

        with open(filepath, "w", newline="") as f:
            if not positions:
                return False
            fieldnames = [
                "symbol",
                "quantity",
                "purchase_price",
                "purchase_date",
                "notes",
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(positions)
        return True
    except Exception:
        return False

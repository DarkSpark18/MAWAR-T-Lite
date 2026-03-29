import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import streamlit as st


@st.cache_data(ttl=60)
def fetch_stock_info(ticker: str) -> Optional[Dict]:
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        if not info or "regularMarketPrice" not in info:
            return None

        return {
            "symbol": info.get("symbol", ticker.upper()),
            "name": info.get("longName", info.get("shortName", ticker.upper())),
            "price": info.get("regularMarketPrice", 0),
            "change": info.get("regularMarketChange", 0),
            "change_pct": info.get("regularMarketChangePercent", 0),
            "volume": info.get("regularMarketVolume", 0),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "eps": info.get("trailingEps", 0),
            "high_52w": info.get("fiftyTwoWeekHigh", 0),
            "low_52w": info.get("fiftyTwoWeekLow", 0),
            "avg_volume": info.get("averageVolume", 0),
            "sector": info.get("sector", "N/A"),
            "industry": info.get("industry", "N/A"),
            "description": info.get("longBusinessSummary", "")[:500],
            "beta": info.get("beta", 0),
            "dividend_yield": info.get("dividendYield", 0) or 0,
        }
    except Exception as e:
        return None


@st.cache_data(ttl=300)
def fetch_historical_data(ticker: str, period: str = "1Y") -> Optional[pd.DataFrame]:
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period)

        if df.empty:
            return None

        df.index = df.index.tz_localize(None)
        return df
    except Exception:
        return None


@st.cache_data(ttl=60)
def fetch_multiple_stocks(tickers: List[str]) -> Dict[str, Dict]:
    result = {}

    for ticker in tickers:
        info = fetch_stock_info(ticker)
        if info:
            result[ticker.upper()] = info

    return result


def get_historical_prices(ticker: str, days: int = 252) -> Optional[np.ndarray]:
    df = fetch_historical_data(ticker, period=f"{days}D")
    if df is not None and not df.empty:
        return df["Close"].values
    return None


def get_returns_data(ticker: str, days: int = 252) -> Tuple[float, float]:
    prices = get_historical_prices(ticker, days)

    if prices is None or len(prices) < 2:
        return 0.0, 0.0

    returns = np.diff(prices) / prices[:-1]
    mean_return = float(np.mean(returns))
    volatility = float(np.std(returns))

    return mean_return, volatility


def search_stocks(query: str) -> List[Dict]:
    query = query.upper().strip()
    if not query:
        return []

    try:
        tickers = yf.Tickers(query)
        info = tickers.tickers.get(query.upper())

        if info and info.info:
            return [
                {
                    "symbol": info.info.get("symbol", query),
                    "name": info.info.get("longName", query),
                    "exchange": info.info.get("exchange", "N/A"),
                }
            ]
    except Exception:
        pass

    return []


def validate_ticker_exists(ticker: str) -> bool:
    info = fetch_stock_info(ticker)
    return info is not None


def get_market_status() -> Dict:
    now = datetime.now()
    hour = now.hour

    weekday = now.weekday()
    is_weekend = weekday >= 5

    market_open = 9 <= hour < 16 and not is_weekend

    return {
        "is_open": market_open,
        "is_weekend": is_weekend,
        "next_open": "Monday 9:00 AM" if is_weekend else None,
    }

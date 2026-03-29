import streamlit as st
from typing import Optional

from config.theme import (
    BBG_PANEL,
    BBG_PANEL_BORDER,
    BBG_TEXT,
    BBG_TEXT_DIM,
    BBG_ORANGE,
    BBG_GREEN,
    BBG_RED,
)


def render_stock_card(
    symbol: str,
    name: str,
    price: float,
    change: float,
    change_pct: float,
    is_pinned: bool = False,
    on_click: Optional[callable] = None,
):
    change_color = BBG_GREEN if change >= 0 else BBG_RED
    change_sign = "+" if change >= 0 else ""

    st.markdown(
        f"""
    <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 15px; margin: 5px 0;">
        <div style="display: flex; justify-content: space-between; align-items: start;">
            <div>
                <div style="color: {"#FF9900" if is_pinned else "#00AAFF"}; font-weight: 700; font-size: 16px; font-family: 'JetBrains Mono', monospace;">
                    {symbol}
                </div>
                <div style="color: {BBG_TEXT_DIM}; font-size: 10px; font-family: 'JetBrains Mono', monospace; max-width: 180px; overflow: hidden; text-overflow: ellipsis;">
                    {name}
                </div>
            </div>
            <div style="text-align: right;">
                <div style="color: {BBG_TEXT}; font-size: 18px; font-weight: 700; font-family: 'JetBrains Mono', monospace;">${price:.2f}</div>
                <div style="color: {change_color}; font-size: 12px; font-family: 'JetBrains Mono', monospace;">{change_sign}{change:.2f} ({change_sign}{change_pct:.2f}%)</div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    if on_click:
        if st.button("PIN" if not is_pinned else "UNPIN", key=f"pin_{symbol}"):
            on_click(symbol)


def render_bbg_ticker_row(
    symbol: str,
    price: float,
    change_pct: float,
    volume: str = None,
    market_cap: str = None,
):
    change_color = BBG_GREEN if change_pct >= 0 else BBG_RED
    change_sign = "+" if change_pct >= 0 else ""

    st.markdown(
        f"""
    <div style="display: grid; grid-template-columns: 80px 1fr 100px 100px {f"{100}px" if volume else ""} {f"{100}px" if market_cap else ""}; gap: 15px; padding: 10px 0; border-bottom: 1px solid {BBG_PANEL_BORDER}; font-family: 'JetBrains Mono', monospace; font-size: 12px; align-items: center;">
        <span style="color: #00AAFF; font-weight: 700;">{symbol}</span>
        <span style="color: {BBG_TEXT}; font-weight: 600;">${price:.2f}</span>
        <span style="color: {change_color};">{change_sign}{change_pct:.2f}%</span>
        {f'<span style="color: {BBG_TEXT_DIM};">{volume}</span>' if volume else ""}
        {f'<span style="color: {BBG_TEXT_DIM};">{market_cap}</span>' if market_cap else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )

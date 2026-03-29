import streamlit as st
import pandas as pd
from datetime import datetime
from typing import Optional

from config.stocks_list import TOP_STOCKS
from config.theme import (
    CUSTOM_CSS,
    PRIMARY_ORANGE,
    BACKGROUND_CARD,
    TEXT_SECONDARY,
    SUCCESS_GREEN,
    DANGER_RED,
    ACCENT_BLUE,
    BBG_BLACK,
    BBG_DARK_GRAY,
    BBG_PANEL,
    BBG_ORANGE,
    BBG_TEXT,
    BBG_TEXT_DIM,
    BBG_PANEL_BORDER,
    BBG_GREEN,
    BBG_RED,
)
from modules.data_fetcher import (
    fetch_multiple_stocks,
    fetch_stock_info,
    fetch_historical_data,
)
from utils.storage import load_pinned_stocks, pin_stock, unpin_stock
from utils.charts import create_price_line_chart


def render_header():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.markdown(
            f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="color: {BBG_ORANGE}; font-size: 32px;">📊</span>
            <div>
                <span style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; letter-spacing: 2px;">
                    MAWAR T LITE
                </span>
                <span style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-left: 10px;">
                    TERMINAL
                </span>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )
    with col3:
        now = datetime.now()
        st.markdown(
            f"""
        <div style="text-align: right;">
            <div style="color: {BBG_TEXT}; font-family: 'JetBrains Mono', monospace; font-size: 12px;">{now.strftime("%d %b %Y")}</div>
            <div style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 600;">{now.strftime("%H:%M:%S")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<hr style="border-color: {BBG_PANEL_BORDER}; border-width: 2px;">',
        unsafe_allow_html=True,
    )


def display_pinned_stocks():
    pinned = load_pinned_stocks()

    if not pinned:
        return

    st.markdown(
        f"""
    <div style="background-color: {BBG_DARK_GRAY}; border: 1px solid {BBG_PANEL_BORDER}; margin-bottom: 15px;">
        <div style="background-color: {BBG_PANEL}; color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-transform: uppercase; font-size: 11px; padding: 8px 15px; border-bottom: 1px solid {BBG_PANEL_BORDER};">
            PINNED WATCHLIST
        </div>
        <div style="padding: 10px 15px; display: flex; gap: 15px; overflow-x: auto;">
    """,
        unsafe_allow_html=True,
    )

    stocks_data = fetch_multiple_stocks(pinned)

    for symbol in pinned:
        stock = stocks_data.get(symbol, {})
        if stock:
            change = stock.get("change_pct", 0)
            change_color = BBG_GREEN if change >= 0 else BBG_RED
            change_sign = "+" if change >= 0 else ""

            st.markdown(
                f"""
            <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 12px; min-width: 120px; text-align: center;">
                <div style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 14px;">{symbol}</div>
                <div style="color: {BBG_TEXT}; font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 600;">${stock.get("price", 0):.2f}</div>
                <div style="color: {change_color}; font-family: 'JetBrains Mono', monospace; font-size: 11px;">{change_sign}{change:.2f}%</div>
                <button onclick="window.location.href='#'" style="background: transparent; border: none; color: {BBG_TEXT_DIM}; font-size: 10px; cursor: pointer; margin-top: 5px;">UNPIN</button>
            </div>
            """,
                unsafe_allow_html=True,
            )

    st.markdown("</div></div>", unsafe_allow_html=True)

    for symbol in pinned:
        if st.button(f"UNPIN {symbol}", key=f"unpin_{symbol}"):
            unpin_stock(symbol)
            st.rerun()


def display_top_stocks(search_query: str = "") -> pd.DataFrame:
    symbols = [s["symbol"] for s in TOP_STOCKS]
    stocks_data = fetch_multiple_stocks(symbols)

    records = []
    for stock_info in TOP_STOCKS:
        symbol = stock_info["symbol"]
        stock = stocks_data.get(symbol, {})

        if search_query and search_query.upper() not in symbol.upper():
            continue

        records.append(
            {
                "Symbol": symbol,
                "Name": stock_info["name"],
                "Price": stock.get("price", 0),
                "Change": stock.get("change_pct", 0),
                "Volume": stock.get("volume", 0),
                "Mkt Cap": stock.get("market_cap", 0),
                "P/E": stock.get("pe_ratio", 0),
            }
        )

    if not records:
        st.info("No stocks found")
        return pd.DataFrame()

    return pd.DataFrame(records)


def render_stocks_table(df: pd.DataFrame):
    if df.empty:
        return

    st.markdown(
        f"""
    <div style="background-color: {BBG_DARK_GRAY}; border: 1px solid {BBG_PANEL_BORDER}; margin: 15px 0;">
        <div style="background-color: {BBG_PANEL}; color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-transform: uppercase; font-size: 11px; padding: 8px 15px; border-bottom: 1px solid {BBG_PANEL_BORDER};">
            TOP 50 GLOBAL STOCKS
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        df,
        column_config={
            "Symbol": st.column_config.TextColumn("SYMBOL", width="small"),
            "Name": st.column_config.TextColumn("NAME", width="medium"),
            "Price": st.column_config.NumberColumn(
                "LAST", format="$%.2f", width="small"
            ),
            "Change": st.column_config.NumberColumn(
                "CHG %", format="%.2f%%", width="small"
            ),
            "Volume": st.column_config.TextColumn("VOLUME", width="small"),
            "Mkt Cap": st.column_config.TextColumn("MKT CAP", width="small"),
            "P/E": st.column_config.NumberColumn("P/E", format="%.2f", width="small"),
        },
        hide_index=True,
        use_container_width=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)


def display_stock_details(symbol: str):
    stock = fetch_stock_info(symbol)

    if not stock:
        st.error(f"Unable to fetch data for {symbol}")
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("LAST", f"${stock['price']:.2f}")
    with col2:
        st.metric("CHG", f"${stock['change']:+.2f}", f"{stock['change_pct']:+.2f}%")
    with col3:
        vol = stock["volume"]
        st.metric("VOLUME", f"{vol / 1e6:.2f}M" if vol > 1e6 else f"{vol / 1e3:.0f}K")
    with col4:
        mkt = stock["market_cap"]
        st.metric(
            "MKT CAP", f"${mkt / 1e12:.2f}T" if mkt > 1e12 else f"${mkt / 1e9:.2f}B"
        )

    st.markdown(
        f'<hr style="border-color: {BBG_PANEL_BORDER};">', unsafe_allow_html=True
    )

    tabs = st.tabs(["CHART", "STATISTICS", "ABOUT"])

    with tabs[0]:
        period = st.selectbox("PERIOD", ["1W", "1M", "3M", "6M", "1Y", "5Y"], index=4)
        period_map = {
            "1W": "5D",
            "1M": "1Mo",
            "3M": "3Mo",
            "6M": "6Mo",
            "1Y": "1Y",
            "5Y": "5Y",
        }

        df = fetch_historical_data(symbol, period_map.get(period, "1Y"))
        if df is not None:
            fig = create_price_line_chart(
                df.index.tolist(), df["Close"].tolist(), f"{symbol} PRICE"
            )
            st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(
                f"""
            <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 15px;">
                <div style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; margin-bottom: 10px;">VALUATION</div>
                <div style="display: grid; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
                    <div style="display: flex; justify-content: space-between;"><span style="color: {BBG_TEXT_DIM};">P/E RATIO</span><span style="color: {BBG_TEXT};">{stock["pe_ratio"]:.2f}</span></div>
                    <div style="display: flex; justify-content: space-between;"><span style="color: {BBG_TEXT_DIM};">EPS</span><span style="color: {BBG_TEXT};">${stock["eps"]:.2f}</span></div>
                    <div style="display: flex; justify-content: space-between;"><span style="color: {BBG_TEXT_DIM};">BETA</span><span style="color: {BBG_TEXT};">{stock["beta"]:.2f}</span></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f"""
            <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 15px;">
                <div style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; margin-bottom: 10px;">52W RANGE</div>
                <div style="display: grid; gap: 8px; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
                    <div style="display: flex; justify-content: space-between;"><span style="color: {BBG_TEXT_DIM};">HIGH</span><span style="color: {BBG_GREEN};">${stock["high_52w"]:.2f}</span></div>
                    <div style="display: flex; justify-content: space-between;"><span style="color: {BBG_TEXT_DIM};">LOW</span><span style="color: {BBG_RED};">${stock["low_52w"]:.2f}</span></div>
                    <div style="display: flex; justify-content: space-between;"><span style="color: {BBG_TEXT_DIM};">DIV YIELD</span><span style="color: {BBG_TEXT};">{stock["dividend_yield"] * 100:.2f}%</span></div>
                </div>
            </div>
            """,
                unsafe_allow_html=True,
            )

    with tabs[2]:
        st.markdown(
            f"""
        <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 15px; font-family: 'JetBrains Mono', monospace;">
            <div style="color: {BBG_ORANGE}; font-size: 14px; font-weight: 600; margin-bottom: 10px;">{stock["name"]}</div>
            <div style="color: {BBG_TEXT_DIM}; font-size: 11px; margin-bottom: 15px;">
                <span style="color: {BBG_TEXT}; margin-right: 20px;">SECTOR: {stock["sector"]}</span>
                <span style="color: {BBG_TEXT};">INDUSTRY: {stock["industry"]}</span>
            </div>
            <div style="color: {BBG_TEXT}; font-size: 12px; line-height: 1.6;">{stock.get("description", "No description available.")}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )


def handle_pin_unpin(symbol: str):
    pinned = load_pinned_stocks()

    if symbol in pinned:
        unpin_stock(symbol)
        st.success(f"Removed {symbol} from pinned stocks")
    else:
        if len(pinned) >= 5:
            st.warning("Maximum 5 stocks can be pinned")
        else:
            pin_stock(symbol)
            st.success(f"Added {symbol} to pinned stocks")

    st.rerun()


def dashboard_page():
    render_header()
    display_pinned_stocks()

    col_search, col_pin = st.columns([4, 1])
    with col_search:
        search_query = st.text_input("SEARCH", placeholder="Enter symbol (e.g., AAPL)")
    with col_pin:
        st.markdown("&nbsp;")
        selected_stock = st.selectbox(
            "DETAILS", ["Select..."] + [s["symbol"] for s in TOP_STOCKS]
        )

    df = display_top_stocks(search_query)

    if not df.empty:
        render_stocks_table(df)

    if selected_stock != "Select...":
        st.markdown(
            f'<hr style="border-color: {BBG_PANEL_BORDER}; border-width: 2px; margin-top: 30px;">',
            unsafe_allow_html=True,
        )
        st.markdown(
            f"""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
            <span style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 14px; text-transform: uppercase; letter-spacing: 1px;">{selected_stock} DETAILS</span>
            <button onclick="alert('Pin feature coming soon')" style="background-color: {BBG_PANEL}; color: {BBG_TEXT}; border: 1px solid {BBG_PANEL_BORDER}; padding: 5px 15px; cursor: pointer; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; font-size: 10px;">PIN TO WATCHLIST</button>
        </div>
        """,
            unsafe_allow_html=True,
        )
        display_stock_details(selected_stock)

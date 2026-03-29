import streamlit as st
import pandas as pd
from datetime import datetime, date
from typing import Dict, List

from config.theme import (
    CUSTOM_CSS,
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
from modules.data_fetcher import fetch_stock_info, fetch_multiple_stocks
from utils.storage import (
    load_portfolio,
    add_position,
    update_position,
    delete_position,
    export_to_csv,
)
from utils.calculations import (
    calculate_portfolio_value,
    calculate_portfolio_cost,
    calculate_total_pnl,
    calculate_position_pnl,
    calculate_portfolio_allocation,
    format_currency,
)
from utils.charts import create_allocation_pie_chart
from utils.validators import validate_portfolio_position


def render_bbg_panel(title: str):
    st.markdown(
        f"""
    <div style="background-color: {BBG_DARK_GRAY}; border: 1px solid {BBG_PANEL_BORDER}; margin: 10px 0;">
        <div style="background-color: {BBG_PANEL}; color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-transform: uppercase; font-size: 11px; padding: 8px 15px; border-bottom: 1px solid {BBG_PANEL_BORDER}; letter-spacing: 1px;">
            {title}
        </div>
        <div style="padding: 15px;">
    """,
        unsafe_allow_html=True,
    )


def end_bbg_panel():
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_portfolio_summary(positions: List[Dict], current_prices: Dict[str, float]):
    if not positions:
        st.info("No positions in portfolio. Add your first position below.")
        return

    pnl_data = calculate_total_pnl(positions, current_prices)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("PORTFOLIO VALUE", format_currency(pnl_data["total_value"]))
    with col2:
        st.metric("TOTAL COST", format_currency(pnl_data["total_cost"]))
    with col3:
        sign = "+" if pnl_data["pnl"] >= 0 else ""
        st.metric(
            "TOTAL P&L",
            f"{sign}{format_currency(pnl_data['pnl'])}",
            f"{sign}{pnl_data['pnl_pct']:.2f}%",
        )
    with col4:
        st.metric("POSITIONS", str(len(positions)))


def render_positions_table(positions: List[Dict], current_prices: Dict[str, float]):
    if not positions:
        return

    records = []
    for pos in positions:
        symbol = pos.get("symbol", "").upper()
        current_price = current_prices.get(symbol, 0)
        pnl = calculate_position_pnl(pos, current_price)

        change_pct = (
            (current_price / pos.get("purchase_price", 1) - 1) * 100
            if pos.get("purchase_price", 0)
            else 0
        )

        records.append(
            {
                "id": pos.get("id"),
                "Symbol": symbol,
                "Qty": pos.get("quantity"),
                "Avg Cost": pos.get("purchase_price", 0),
                "Last": current_price,
                "Value": pnl["current_value"],
                "P&L $": pnl["pnl"],
                "P&L %": change_pct,
                "Date": pos.get("purchase_date", "N/A"),
            }
        )

    df = pd.DataFrame(records)

    st.dataframe(
        df.drop(columns=["id"]),
        column_config={
            "Symbol": st.column_config.TextColumn("SYMBOL", width="small"),
            "Qty": st.column_config.NumberColumn("QTY", format="%.2f", width="small"),
            "Avg Cost": st.column_config.NumberColumn(
                "AVG COST", format="$%.2f", width="small"
            ),
            "Last": st.column_config.NumberColumn(
                "LAST", format="$%.2f", width="small"
            ),
            "Value": st.column_config.NumberColumn(
                "VALUE", format="$%.2f", width="small"
            ),
            "P&L $": st.column_config.NumberColumn(
                "P&L $", format="$%.2f", width="small"
            ),
            "P&L %": st.column_config.NumberColumn(
                "P&L %", format="%.2f%%", width="small"
            ),
            "Date": st.column_config.TextColumn("DATE", width="small"),
        },
        hide_index=True,
        use_container_width=True,
    )


def render_add_position_form():
    render_bbg_panel("ADD POSITION")

    with st.form("add_position_form"):
        col1, col2 = st.columns(2)

        with col1:
            symbol = st.text_input("SYMBOL", placeholder="e.g., AAPL").upper()
            quantity = st.number_input(
                "QUANTITY", min_value=0.01, step=0.01, format="%.2f"
            )

        with col2:
            purchase_price = st.number_input(
                "PURCHASE PRICE ($)", min_value=0.01, step=0.01, format="%.2f"
            )
            purchase_date = st.date_input("DATE", value=date.today())

        notes = st.text_area("NOTES (OPTIONAL)", placeholder="Any notes...")

        submitted = st.form_submit_button("ADD POSITION", use_container_width=True)

        if submitted:
            position = {
                "symbol": symbol,
                "quantity": quantity,
                "purchase_price": purchase_price,
                "purchase_date": purchase_date.isoformat(),
                "notes": notes,
            }

            is_valid, error = validate_portfolio_position(position)

            if not is_valid:
                st.error(error)
            else:
                stock = fetch_stock_info(symbol)
                if not stock:
                    st.error(f"Could not validate symbol: {symbol}")
                else:
                    add_position(position)
                    st.success(
                        f"Added {quantity} shares of {symbol} at ${purchase_price}"
                    )
                    st.rerun()

    end_bbg_panel()


def render_edit_delete_buttons(positions: List[Dict]):
    if not positions:
        return

    render_bbg_panel("MANAGE POSITIONS")

    for idx, pos in enumerate(positions):
        pos_id = pos.get("id", f"legacy_{idx}")
        with st.expander(f"{pos.get('symbol', 'Unknown')}"):
            col1, col2 = st.columns([1, 1])

            with col1:
                quantity = st.number_input(
                    "QTY",
                    min_value=0.01,
                    value=float(pos.get("quantity", 1)),
                    key=f"qty_{pos_id}",
                )
                price = st.number_input(
                    "PRICE",
                    min_value=0.01,
                    value=float(pos.get("purchase_price", 0)),
                    key=f"price_{pos_id}",
                )

                if st.button("UPDATE", key=f"update_{pos_id}"):
                    update_position(
                        pos_id,
                        {
                            "quantity": quantity,
                            "purchase_price": price,
                        },
                    )
                    st.success("Position updated")
                    st.rerun()

            with col2:
                st.write(f"**DATE:** {pos.get('purchase_date', 'N/A')}")
                st.write(f"**NOTES:** {pos.get('notes', 'None')}")

                if st.button("DELETE", key=f"delete_{pos_id}", type="primary"):
                    delete_position(pos_id)
                    st.success("Position deleted")
                    st.rerun()

    end_bbg_panel()


def render_export_section(positions: List[Dict]):
    render_bbg_panel("EXPORT")

    if st.button("EXPORT TO CSV", use_container_width=True):
        if not positions:
            st.warning("No positions to export")
        else:
            filepath = "portfolio_export.csv"
            if export_to_csv(positions, filepath):
                st.success(f"Portfolio exported to {filepath}")
                with open(filepath, "rb") as f:
                    st.download_button(
                        "DOWNLOAD", f, file_name="portfolio.csv", mime="text/csv"
                    )
            else:
                st.error("Failed to export portfolio")

    end_bbg_panel()


def portfolio_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.markdown(
        f"""
    <div style="border-left: 3px solid {BBG_ORANGE}; padding-left: 15px; margin: 20px 0;">
        <h1 style="color: {BBG_TEXT}; margin: 0; font-size: 20px; text-transform: uppercase; letter-spacing: 2px;">
            Portfolio Manager
        </h1>
        <div style="color: {BBG_TEXT_DIM}; font-size: 11px; margin-top: 5px; text-transform: uppercase;">
            Track your investments and analyze performance
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    positions = load_portfolio()
    symbols = list(set(pos.get("symbol", "").upper() for pos in positions))
    current_prices = fetch_multiple_stocks(symbols)
    current_prices = {s: data.get("price", 0) for s, data in current_prices.items()}

    render_bbg_panel("PORTFOLIO SUMMARY")
    render_portfolio_summary(positions, current_prices)
    end_bbg_panel()

    tab1, tab2, tab3, tab4 = st.tabs(["POSITIONS", "ADD/EDIT", "EXPORT", "ANALYSIS"])

    with tab1:
        render_bbg_panel("ALL POSITIONS")
        render_positions_table(positions, current_prices)
        end_bbg_panel()

    with tab2:
        render_add_position_form()
        render_edit_delete_buttons(positions)

    with tab3:
        render_export_section(positions)

    with tab4:
        render_bbg_panel("ALLOCATION")
        allocation = calculate_portfolio_allocation(positions, current_prices)
        if allocation:
            fig = create_allocation_pie_chart(allocation)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add positions to see allocation chart")
        end_bbg_panel()

    st.markdown(
        f"""
    <div style="background-color: {BBG_DARK_GRAY}; border-top: 1px solid {BBG_PANEL_BORDER}; padding: 15px; margin-top: 40px; text-align: center;">
        <div style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">
            MAWAR T LITE | DATA PROVIDED BY YAHOO FINANCE | FOR EDUCATIONAL PURPOSES ONLY
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

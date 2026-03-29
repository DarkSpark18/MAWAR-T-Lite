import streamlit as st
import numpy as np
from datetime import datetime, timedelta
from typing import Tuple

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
    BBG_BLUE,
)
from config.settings import DEFAULT_SIMULATIONS, DEFAULT_CONFIDENCE
from modules.data_fetcher import fetch_stock_info, get_returns_data
from utils.calculations import (
    monte_carlo_simulation,
    get_confidence_intervals,
    format_currency,
    format_percentage,
)
from utils.charts import create_monte_carlo_chart, create_distribution_histogram
from utils.validators import validate_ticker


def render_bbg_panel(title: str):
    st.html(
        f"""
        <div style="background-color: {BBG_DARK_GRAY}; border: 1px solid {BBG_PANEL_BORDER}; margin: 10px 0; padding: 0; border-radius: 4px; overflow: hidden;">
            <div style="background-color: {BBG_PANEL}; color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-transform: uppercase; font-size: 11px; padding: 8px 15px; border-bottom: 1px solid {BBG_PANEL_BORDER}; letter-spacing: 1px;">
                {title}
            </div>
            <div style="padding: 15px;">
        """
    )


def end_bbg_panel():
    st.html("</div></div>")


def stock_selection_ui():
    st.html(
        """
        <div style="background-color: #1A1A1A; border: 1px solid #333333; padding: 15px; margin: 10px 0;">
            <div style="color: #FF9900; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; margin-bottom: 10px;">STOCK SELECTION</div>
        </div>
        """
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        ticker_input = st.text_input("ENTER TICKER", placeholder="e.g., AAPL")
        ticker = ticker_input.upper().strip() if ticker_input else ""

    with col2:
        st.markdown("&nbsp;")
        if ticker and validate_ticker(ticker):
            stock = fetch_stock_info(ticker)
            if stock:
                st.success(f"VALIDATED: {stock['name']}")
            else:
                st.error("Invalid ticker")

    return ticker if ticker and validate_ticker(ticker) else None


def simulation_parameters_ui():
    st.html(
        f'<div style="color: {BBG_ORANGE}; font-family: "JetBrains Mono", monospace; font-size: 11px; text-transform: uppercase; margin: 20px 0 10px 0;">SIMULATION PARAMETERS</div>'
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        days = st.selectbox("PERIOD (DAYS)", [30, 60, 90, 180, 365], index=2)

    with col2:
        simulations = st.slider(
            "SIMULATIONS", 100, 10000, DEFAULT_SIMULATIONS, step=100
        )

    with col3:
        confidence = st.selectbox("CONFIDENCE", [68, 95, 99], index=1)

    return days, simulations, confidence


def run_monte_carlo(initial_price, mean_return, volatility, days, simulations) -> Tuple:
    price_paths, final_prices = monte_carlo_simulation(
        initial_price=initial_price,
        days=days,
        simulations=simulations,
        volatility=volatility,
        mean_return=mean_return,
    )
    return price_paths, final_prices


def display_simulation_results(
    current_price, final_prices, price_paths, days, confidence
):
    confidence_intervals = get_confidence_intervals(final_prices, confidence)
    lower, median, upper = confidence_intervals

    expected_return = np.mean(final_prices)
    return_pct = ((expected_return - current_price) / current_price) * 100

    p10 = np.percentile(final_prices, 10)
    p90 = np.percentile(final_prices, 90)

    downside = np.sum(final_prices < current_price) / len(final_prices) * 100
    upside = np.sum(final_prices > current_price) / len(final_prices) * 100

    render_bbg_panel("SIMULATION RESULTS")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "EXPECTED PRICE",
            format_currency(expected_return),
            f"{'+' if return_pct >= 0 else ''}{return_pct:.2f}%",
        )

    with col2:
        st.html(
            f"""
        <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 15px; text-align: center;">
            <div style="color: {BBG_TEXT_DIM}; font-size: 10px; text-transform: uppercase;">{confidence}% CI RANGE</div>
            <div style="color: {BBG_RED}; font-size: 16px; font-weight: 600;">{format_currency(lower)}</div>
            <div style="color: {BBG_TEXT_DIM}; font-size: 10px;">to</div>
            <div style="color: {BBG_GREEN}; font-size: 16px; font-weight: 600;">{format_currency(upper)}</div>
        </div>
        """
        )

    with col3:
        st.html(
            f"""
        <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 15px; text-align: center;">
            <div style="color: {BBG_TEXT_DIM}; font-size: 10px; text-transform: uppercase;">P10-P90 RANGE</div>
            <div style="color: {BBG_RED}; font-size: 16px; font-weight: 600;">{format_currency(p10)}</div>
            <div style="color: {BBG_TEXT_DIM}; font-size: 10px;">to</div>
            <div style="color: {BBG_GREEN}; font-size: 16px; font-weight: 600;">{format_currency(p90)}</div>
        </div>
        """
        )

    with col4:
        st.html(
            f"""
        <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 15px; text-align: center;">
            <div style="color: {BBG_GREEN}; font-size: 16px; font-weight: 600;">{upside:.1f}%</div>
            <div style="color: {BBG_TEXT_DIM}; font-size: 10px; text-transform: uppercase;">UPSIDE</div>
            <div style="color: {BBG_RED}; font-size: 16px; font-weight: 600;">{downside:.1f}%</div>
            <div style="color: {BBG_TEXT_DIM}; font-size: 10px; text-transform: uppercase;">DOWNSIDE</div>
        </div>
        """
        )

    end_bbg_panel()

    tab1, tab2 = st.tabs(["PRICE PATHS", "DISTRIBUTION"])

    with tab1:
        dates = [datetime.now() + timedelta(days=i) for i in range(days + 1)]
        fig = create_monte_carlo_chart(price_paths, dates, confidence_intervals)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        fig = create_distribution_histogram(final_prices, current_price)
        st.plotly_chart(fig, use_container_width=True)


def display_risk_metrics(final_prices, current_price):
    render_bbg_panel("RISK METRICS")

    var_95 = np.percentile(final_prices, 5)
    var_99 = np.percentile(final_prices, 1)

    max_loss = np.min(final_prices)
    max_gain = np.max(final_prices)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("VaR (95%)", format_currency(current_price - var_95))

    with col2:
        st.metric("VaR (99%)", format_currency(current_price - var_99))

    with col3:
        st.metric(
            "WORST CASE",
            format_currency(max_loss),
            f"{((max_loss / current_price - 1) * 100):+.2f}%",
        )

    with col4:
        st.metric(
            "BEST CASE",
            format_currency(max_gain),
            f"{((max_gain / current_price - 1) * 100):+.2f}%",
        )

    end_bbg_panel()


def predictor_page():
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

    st.html(
        f"""
        <div style="border-left: 3px solid {BBG_ORANGE}; padding-left: 15px; margin: 20px 0;">
            <h1 style="color: {BBG_TEXT}; margin: 0; font-size: 20px; text-transform: uppercase; letter-spacing: 2px;">
                Monte Carlo Predictor
            </h1>
            <div style="color: {BBG_TEXT_DIM}; font-size: 11px; margin-top: 5px; text-transform: uppercase;">
                Statistical price predictions using Monte Carlo simulation
            </div>
        </div>
        """
    )

    ticker = stock_selection_ui()

    if not ticker:
        render_bbg_panel("HOW IT WORKS")
        st.html(
            f"""
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: {BBG_TEXT}; line-height: 1.8;">
                <p>Monte Carlo simulation uses <span style="color: {BBG_ORANGE};">historical volatility</span> and <span style="color: {BBG_ORANGE};">returns</span> to generate thousands of possible future price paths.</p>
                
                <div style="background-color: {BBG_PANEL}; padding: 15px; margin: 15px 0; border-left: 2px solid {BBG_ORANGE};">
                    <div style="color: {BBG_ORANGE}; font-size: 11px; text-transform: uppercase; margin-bottom: 10px;">KEY PARAMETERS</div>
                    <ul style="margin: 0; padding-left: 20px; color: {BBG_TEXT_DIM};">
                        <li><span style="color: {BBG_TEXT};">PREDICTION PERIOD</span> - How far into the future to predict</li>
                        <li><span style="color: {BBG_TEXT};">SIMULATIONS</span> - More = more accurate (but slower)</li>
                        <li><span style="color: {BBG_TEXT};">CONFIDENCE LEVEL</span> - Probability range for predictions</li>
                    </ul>
                </div>
                
                <div style="background-color: {BBG_PANEL}; padding: 15px; margin: 15px 0; border-left: 2px solid {BBG_BLUE};">
                    <div style="color: {BBG_BLUE}; font-size: 11px; text-transform: uppercase; margin-bottom: 10px;">INTERPRETING RESULTS</div>
                    <ul style="margin: 0; padding-left: 20px; color: {BBG_TEXT_DIM};">
                        <li><span style="color: {BBG_TEXT};">EXPECTED PRICE</span> - Average of all simulated outcomes</li>
                        <li><span style="color: {BBG_TEXT};">CONFIDENCE INTERVAL</span> - Range where price likely falls</li>
                        <li><span style="color: {BBG_TEXT};">UPSIDE/DOWNSIDE</span> - Probability of gaining or losing</li>
                    </ul>
                </div>
            </div>
            """
        )
        end_bbg_panel()
        return

    stock = fetch_stock_info(ticker)

    if not stock:
        st.error(f"Could not fetch data for {ticker}")
        return

    render_bbg_panel("CURRENT DATA")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("LAST", format_currency(stock["price"]))
    with col2:
        st.metric("52W HIGH", format_currency(stock["high_52w"]))
    with col3:
        st.metric("52W LOW", format_currency(stock["low_52w"]))
    end_bbg_panel()

    days, simulations, confidence = simulation_parameters_ui()

    with st.spinner("Fetching historical data..."):
        mean_return, volatility = get_returns_data(ticker, days=252)

    if volatility == 0:
        st.error("Insufficient historical data for simulation")
        return

    render_bbg_panel("HISTORICAL SUMMARY")
    st.html(
        f"""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
            <div><span style="color: {BBG_TEXT_DIM};">MEAN DAILY RETURN</span><br><span style="color: {BBG_TEXT}; font-weight: 600;">{mean_return * 100:.4f}%</span></div>
            <div><span style="color: {BBG_TEXT_DIM};">DAILY VOLATILITY</span><br><span style="color: {BBG_TEXT}; font-weight: 600;">{volatility * 100:.4f}%</span></div>
            <div><span style="color: {BBG_TEXT_DIM};">ANNUALIZED VOL</span><br><span style="color: {BBG_TEXT}; font-weight: 600;">{volatility * np.sqrt(252) * 100:.2f}%</span></div>
        </div>
        """
    )
    end_bbg_panel()

    if st.button("RUN SIMULATION", type="primary", use_container_width=True):
        with st.spinner(f"Running {simulations:,} simulations..."):
            price_paths, final_prices = run_monte_carlo(
                initial_price=stock["price"],
                mean_return=mean_return,
                volatility=volatility,
                days=days,
                simulations=simulations,
            )

        display_simulation_results(
            current_price=stock["price"],
            final_prices=final_prices,
            price_paths=price_paths,
            days=days,
            confidence=confidence / 100,
        )

        display_risk_metrics(final_prices, stock["price"])

        st.html(
            f"""
            <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_ORANGE}; padding: 15px; margin-top: 20px;">
                <div style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; margin-bottom: 10px;">DISCLAIMER</div>
                <div style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 11px;">
                    Monte Carlo simulations are based on historical data and do NOT predict future prices with certainty.
                    Use this for educational purposes only, not financial advice.
                </div>
            </div>
            """
        )

import streamlit as st
from datetime import datetime

from config.theme import (
    BBG_BLACK,
    BBG_DARK_GRAY,
    BBG_PANEL,
    BBG_ORANGE,
    BBG_TEXT,
    BBG_TEXT_DIM,
    BBG_PANEL_BORDER,
)
from config.settings import APP_TITLE, APP_VERSION


def render_header():
    st.markdown(
        f"""
    <div style="background-color: {BBG_BLACK}; border-bottom: 2px solid {BBG_ORANGE}; padding: 15px 0; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; padding: 0 20px;">
            <div>
                <span style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 700; letter-spacing: 2px;">
                    {APP_TITLE}
                </span>
                <span style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 11px; margin-left: 15px;">
                    TERMINAL
                </span>
            </div>
            <div style="text-align: right;">
                <div style="color: {BBG_TEXT}; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
                    {datetime.now().strftime("%d %b %Y")}
                </div>
                <div style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 18px; font-weight: 600;">
                    {datetime.now().strftime("%H:%M:%S")}
                </div>
            </div>
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_page_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
    <div style="border-left: 3px solid {BBG_ORANGE}; padding-left: 15px; margin: 20px 0;">
        <h1 style="color: {BBG_TEXT}; margin: 0; font-size: 20px; text-transform: uppercase; letter-spacing: 2px;">
            {title}
        </h1>
        {f'<div style="color: {BBG_TEXT_DIM}; font-size: 11px; margin-top: 5px; text-transform: uppercase;">{subtitle}</div>' if subtitle else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_panel(title: str = "", content: str = ""):
    panel_html = f"""
    <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; margin: 10px 0;">
    """
    if title:
        panel_html += f"""
        <div style="background-color: {BBG_DARK_GRAY}; color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-weight: 600; text-transform: uppercase; font-size: 11px; padding: 8px 12px; border-bottom: 1px solid {BBG_PANEL_BORDER}; letter-spacing: 1px;">
            {title}
        </div>
        """
    panel_html += f"""
        <div style="padding: 10px;">
            {content}
        </div>
    </div>
    """
    return panel_html


def render_ticker_row(
    symbol: str,
    name: str,
    price: float,
    change: float,
    change_pct: float,
    is_pinned: bool = False,
):
    change_color = "#00FF00" if change >= 0 else "#FF0000"
    change_sign = "+" if change >= 0 else ""

    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid {BBG_PANEL_BORDER}; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <span style="color: {"#FF9900" if is_pinned else "#00AAFF"}; font-weight: 700; min-width: 70px;">{symbol}</span>
            <span style="color: {BBG_TEXT_DIM}; font-size: 10px; max-width: 200px; overflow: hidden; text-overflow: ellipsis;">{name}</span>
        </div>
        <div style="display: flex; align-items: center; gap: 30px;">
            <span style="color: {BBG_TEXT}; font-weight: 600;">${price:.2f}</span>
            <span style="color: {change_color}; min-width: 80px; text-align: right;">{change_sign}{change:.2f} ({change_sign}{change_pct:.2f}%)</span>
        </div>
    </div>
    """


def render_footer():
    st.markdown(
        f"""
    <div style="background-color: {BBG_DARK_GRAY}; border-top: 1px solid {BBG_PANEL_BORDER}; padding: 15px; margin-top: 40px; text-align: center;">
        <div style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 1px;">
            {APP_TITLE} v{APP_VERSION} | DATA PROVIDED BY YAHOO FINANCE | FOR EDUCATIONAL PURPOSES ONLY
        </div>
    </div>
    """,
        unsafe_allow_html=True,
    )

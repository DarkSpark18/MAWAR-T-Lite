import streamlit as st
from typing import Optional

from config.theme import (
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


def render_metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: Optional[str] = None,
    help_text: Optional[str] = None,
):
    if delta_color == "normal":
        delta_color = BBG_GREEN
    elif delta_color == "inverse":
        delta_color = BBG_RED

    st.metric(
        label=label.upper(),
        value=value,
        delta=delta,
        delta_color=delta_color,
        help=help_text,
    )


def render_bbg_metric(label: str, value: str, subtext: str = "", color: str = BBG_TEXT):
    st.markdown(
        f"""
    <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 12px;">
        <div style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">
            {label}
        </div>
        <div style="color: {color}; font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700;">
            {value}
        </div>
        {f'<div style="color: {BBG_TEXT_DIM}; font-size: 10px; margin-top: 3px;">{subtext}</div>' if subtext else ""}
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_bbg_stat(
    label: str, value: str, change: float = None, is_bold: bool = False
):
    change_html = ""
    if change is not None:
        change_color = BBG_GREEN if change >= 0 else BBG_RED
        change_sign = "+" if change >= 0 else ""
        change_html = f'<span style="color: {change_color}; margin-left: 10px;">{change_sign}{change:.2f}%</span>'

    value_weight = "700" if is_bold else "500"

    return f"""
    <div style="display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid {BBG_PANEL_BORDER}; font-family: 'JetBrains Mono', monospace; font-size: 12px;">
        <span style="color: {BBG_TEXT_DIM};">{label}</span>
        <span style="color: {BBG_TEXT}; font-weight: {value_weight};">{value}{change_html}</span>
    </div>
    """

import streamlit as st
import os

APP_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(
    page_title="MAWAR T Lite",
    page_icon=f"{APP_DIR}/assets/images/favicon.ico",
    layout="wide",
    initial_sidebar_state="expanded",
)

from config.theme import (
    CUSTOM_CSS,
    BBG_ORANGE,
    BBG_TEXT,
    BBG_TEXT_DIM,
    BBG_PANEL,
    BBG_PANEL_BORDER,
    BBG_DARK_GRAY,
)
from config.settings import APP_TITLE, APP_VERSION

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def render_sidebar():

    st.sidebar.markdown(
        f"""
        <div style="background-color: {BBG_PANEL}; border: 1px solid {BBG_PANEL_BORDER}; padding: 10px; text-align: center; margin-bottom: 15px;">
            <span style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 16px; font-weight: 700; letter-spacing: 2px;">
                MAWAR T
            </span>
            <span style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 10px; display: block;">LITE TERMINAL</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f'<hr style="border-color: {BBG_PANEL_BORDER}; margin: 10px 0;">',
        unsafe_allow_html=True,
    )

    page = st.sidebar.radio(
        "NAVIGATION",
        ["Dashboard", "Portfolio", "Predictor"],
        index=0,
    )

    st.sidebar.markdown(
        f'<hr style="border-color: {BBG_PANEL_BORDER}; margin: 15px 0;">',
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <div style="background-color: {BBG_DARK_GRAY}; border: 1px solid {BBG_PANEL_BORDER}; padding: 10px;">
            <div style="color: {BBG_ORANGE}; font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; margin-bottom: 5px;">About</div>
            <div style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 10px; line-height: 1.5;">
                Multi-metrix Analytics<br>for Wealth, Assets & Risk
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        f"""
        <div style="text-align: center; margin-top: 10px;">
            <span style="color: {BBG_TEXT_DIM}; font-family: 'JetBrains Mono', monospace; font-size: 10px;">
                Version {APP_VERSION}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return page


def main():
    page = render_sidebar()

    if page == "Dashboard":
        from modules.dashboard import dashboard_page

        dashboard_page()
    elif page == "Portfolio":
        from modules.portfolio import portfolio_page

        portfolio_page()
    elif page == "Predictor":
        from modules.predictor import predictor_page

        predictor_page()


if __name__ == "__main__":
    main()

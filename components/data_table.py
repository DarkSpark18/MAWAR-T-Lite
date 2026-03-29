import streamlit as st
from typing import List, Dict, Callable, Optional
import pandas as pd

from config.theme import BACKGROUND_CARD, PRIMARY_ORANGE, ACCENT_BLUE, TEXT_SECONDARY


def render_data_table(
    data: List[Dict],
    columns: List[str],
    key_column: str,
    on_row_click: Optional[Callable] = None,
):
    if not data:
        st.info("No data available")
        return

    df = pd.DataFrame(data)

    st.dataframe(
        df,
        column_config={col: st.column_config.TextColumn(col) for col in columns},
        hide_index=True,
        use_container_width=True,
        on_select="single" if on_row_click else "off",
        selection_mode="single-row" if on_row_click else "off",
    )


def render_sortable_table(
    data: List[Dict],
    columns: List[str],
    sortable_columns: List[str],
    default_sort: str,
    sort_ascending: bool = False,
):
    col_names = {col: col for col in columns}

    if not data:
        st.info("No data available")
        return

    df = pd.DataFrame(data)

    sort_col = st.selectbox("Sort by", sortable_columns)
    sort_dir = st.radio("Direction", ["Ascending", "Descending"]) == "Descending"

    if sort_col in df.columns:
        df = df.sort_values(sort_col, ascending=sort_dir)

    st.dataframe(
        df,
        column_config=col_names,
        hide_index=True,
        use_container_width=True,
    )

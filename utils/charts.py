import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import List, Dict, Optional, Tuple

BBG_GREEN = "#00FF00"
BBG_RED = "#FF0000"
BBG_ORANGE = "#FF9900"
BBG_BLACK = "#000000"
BBG_DARK_GRAY = "#0D0D0D"
BBG_PANEL = "#1A1A1A"
BBG_PANEL_BORDER = "#333333"
BBG_TEXT = "#FFFFFF"
BBG_TEXT_DIM = "#999999"
BBG_BLUE = "#00AAFF"


def create_price_line_chart(
    dates: List, prices: List, title: str = "Price History"
) -> go.Figure:
    fig = go.Figure()

    price_change = prices[-1] - prices[0] if len(prices) > 1 else 0
    line_color = BBG_GREEN if price_change >= 0 else BBG_RED
    fill_color = "rgba(0, 255, 0, 0.1)" if price_change >= 0 else "rgba(255, 0, 0, 0.1)"

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=prices,
            mode="lines",
            name="Price",
            line=dict(color=line_color, width=2),
            fill="tozeroy",
            fillcolor=fill_color,
        )
    )
    fig.update_layout(
        title=dict(text=title, font=dict(color=BBG_ORANGE, family="JetBrains Mono")),
        paper_bgcolor=BBG_BLACK,
        plot_bgcolor=BBG_DARK_GRAY,
        font=dict(color=BBG_TEXT, family="JetBrains Mono"),
        xaxis=dict(gridcolor=BBG_PANEL_BORDER, showgrid=True),
        yaxis=dict(gridcolor=BBG_PANEL_BORDER, showgrid=True),
        height=400,
    )
    return fig


def create_monte_carlo_chart(
    price_paths: np.ndarray,
    dates: List,
    confidence_intervals: Tuple[float, float, float],
) -> go.Figure:
    fig = go.Figure()

    num_paths = min(100, price_paths.shape[0])
    for i in range(num_paths):
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=price_paths[i],
                mode="lines",
                line=dict(color="rgba(255, 153, 0, 0.1)", width=1),
                showlegend=False,
            )
        )

    mean_path = np.mean(price_paths, axis=0)
    lower, median, upper = confidence_intervals

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=mean_path,
            mode="lines",
            name="Mean",
            line=dict(color=BBG_ORANGE, width=3),
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=[upper] * len(dates),
            mode="lines",
            name="95% Upper",
            line=dict(color=BBG_GREEN, width=1, dash="dash"),
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=[lower] * len(dates),
            mode="lines",
            name="95% Lower",
            line=dict(color=BBG_RED, width=1, dash="dash"),
            showlegend=False,
        )
    )

    fig.update_layout(
        title=dict(
            text="Monte Carlo Price Simulation",
            font=dict(color=BBG_ORANGE, family="JetBrains Mono"),
        ),
        paper_bgcolor=BBG_BLACK,
        plot_bgcolor=BBG_DARK_GRAY,
        font=dict(color=BBG_TEXT, family="JetBrains Mono"),
        xaxis=dict(gridcolor=BBG_PANEL_BORDER, showgrid=True),
        yaxis=dict(gridcolor=BBG_PANEL_BORDER, showgrid=True),
        height=500,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=BBG_TEXT),
        ),
    )
    return fig


def create_distribution_histogram(
    final_prices: np.ndarray, current_price: float
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Histogram(
            x=final_prices,
            nbinsx=50,
            marker_color=BBG_ORANGE,
            name="Final Prices",
            opacity=0.7,
        )
    )

    fig.add_vline(
        x=current_price,
        line_dash="dash",
        line_color=BBG_BLUE,
        annotation_text="Current",
        annotation_position="top",
        annotation=dict(font=dict(color=BBG_BLUE, family="JetBrains Mono")),
    )

    fig.update_layout(
        title=dict(
            text="Distribution of Final Prices",
            font=dict(color=BBG_ORANGE, family="JetBrains Mono"),
        ),
        paper_bgcolor=BBG_BLACK,
        plot_bgcolor=BBG_DARK_GRAY,
        font=dict(color=BBG_TEXT, family="JetBrains Mono"),
        xaxis=dict(title="Price", gridcolor=BBG_PANEL_BORDER, showgrid=True),
        yaxis=dict(title="Frequency", gridcolor=BBG_PANEL_BORDER, showgrid=True),
        height=400,
        showlegend=False,
    )
    return fig


def create_allocation_pie_chart(allocation: Dict[str, float]) -> go.Figure:
    if not allocation:
        return go.Figure()

    labels = list(allocation.keys())
    values = list(allocation.values())

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.4,
                marker=dict(
                    colors=[
                        BBG_ORANGE,
                        BBG_GREEN,
                        BBG_BLUE,
                        BBG_RED,
                        "#FFFF00",
                        "#FF00FF",
                    ]
                ),
                textinfo="label+percent",
                textposition="outside",
                textfont=dict(color=BBG_TEXT, family="JetBrains Mono"),
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text="Portfolio Allocation",
            font=dict(color=BBG_ORANGE, family="JetBrains Mono"),
        ),
        paper_bgcolor=BBG_BLACK,
        font=dict(color=BBG_TEXT, family="JetBrains Mono"),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=BBG_TEXT),
        ),
    )
    return fig


def create_performance_timeline(
    dates: List, values: List, benchmark: Optional[List] = None
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=dates,
            y=values,
            mode="lines",
            name="Portfolio",
            line=dict(color=BBG_ORANGE, width=2),
        )
    )

    if benchmark:
        fig.add_trace(
            go.Scatter(
                x=dates,
                y=benchmark,
                mode="lines",
                name="S&P 500",
                line=dict(color=BBG_BLUE, width=1, dash="dash"),
            )
        )

    fig.update_layout(
        title=dict(
            text="Performance Timeline",
            font=dict(color=BBG_ORANGE, family="JetBrains Mono"),
        ),
        paper_bgcolor=BBG_BLACK,
        plot_bgcolor=BBG_DARK_GRAY,
        font=dict(color=BBG_TEXT, family="JetBrains Mono"),
        xaxis=dict(gridcolor=BBG_PANEL_BORDER, showgrid=True),
        yaxis=dict(gridcolor=BBG_PANEL_BORDER, showgrid=True),
        height=400,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=BBG_TEXT),
        ),
    )
    return fig


def create_candlestick_chart(
    dates: List, opens: List, highs: List, lows: List, closes: List, symbol: str = ""
) -> go.Figure:
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=dates,
                open=opens,
                high=highs,
                low=lows,
                close=closes,
                increasing_line_color=BBG_GREEN,
                decreasing_line_color=BBG_RED,
            )
        ]
    )

    fig.update_layout(
        title=dict(
            text=f"{symbol} Price Chart",
            font=dict(color=BBG_ORANGE, family="JetBrains Mono"),
        ),
        paper_bgcolor=BBG_BLACK,
        plot_bgcolor=BBG_DARK_GRAY,
        font=dict(color=BBG_TEXT, family="JetBrains Mono"),
        xaxis=dict(gridcolor=BBG_PANEL_BORDER, rangeslider=dict(visible=False)),
        yaxis=dict(gridcolor=BBG_PANEL_BORDER),
        height=500,
    )
    return fig

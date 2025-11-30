"""
Chart Components
Plotly visualizations for the valuation dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import List
import numpy as np


def create_revenue_ebit_chart(
    current_revenue: float,
    projected_revenues: List[float],
    ebits: List[float],
    theme: str = "light"
) -> go.Figure:
    """
    Create Revenue & EBIT projection chart (combo bar + line)
    """
    bg_color = "white" if theme == "light" else "#1e293b"
    paper_color = "#f5f7fa" if theme == "light" else "#0f172a"
    text_color = "#1f2937" if theme == "light" else "#e5e7eb"
    grid_color = "#e5e7eb" if theme == "light" else "#334155"
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Add Revenue bars
    fig.add_trace(
        go.Bar(
            x=[f"Year {i}" for i in range(6)],
            y=[current_revenue] + projected_revenues,
            name="Revenue",
            marker_color="#3b82f6",
            text=[f"${val:.1f}M" for val in [current_revenue] + projected_revenues],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>Revenue: $%{y:.1f}M<extra></extra>"
        ),
        secondary_y=False
    )
    
    # Add EBIT line
    fig.add_trace(
        go.Scatter(
            x=[f"Year {i}" for i in range(1, 6)],
            y=ebits,
            name="EBIT",
            mode="lines+markers",
            line=dict(color="#10b981", width=3),
            marker=dict(size=10),
            text=[f"${val:.1f}M" for val in ebits],
            hovertemplate="<b>%{x}</b><br>EBIT: $%{y:.1f}M<extra></extra>"
        ),
        secondary_y=True
    )
    
    # Update layout
    fig.update_xaxes(title_text="Year")
    fig.update_yaxes(title_text="Revenue ($M)", secondary_y=False)
    fig.update_yaxes(title_text="EBIT ($M)", secondary_y=True)
    
    fig.update_layout(
        height=450,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor=bg_color,
        paper_bgcolor=paper_color,
        font=dict(size=12, color=text_color),
        xaxis=dict(gridcolor=grid_color),
        yaxis=dict(gridcolor=grid_color),
        yaxis2=dict(gridcolor=grid_color)
    )
    
    return fig


def create_waterfall_chart(
    pv_fcfs: List[float],
    pv_terminal_value: float,
    enterprise_value: float,
    theme: str = "light"
) -> go.Figure:
    """
    Create valuation waterfall chart
    """
    bg_color = "white" if theme == "light" else "#1e293b"
    paper_color = "#f5f7fa" if theme == "light" else "#0f172a"
    text_color = "#1f2937" if theme == "light" else "#e5e7eb"
    grid_color = "#e5e7eb" if theme == "light" else "#334155"
    
    waterfall_measure = ["relative"] * 5 + ["relative", "total"]
    waterfall_x = [f"Year {i} FCF" for i in range(1, 6)] + ["Terminal Value", "Enterprise Value"]
    waterfall_y = pv_fcfs + [pv_terminal_value, 0]
    waterfall_text = [f"${val:.1f}M" for val in pv_fcfs] + [f"${pv_terminal_value:.1f}M", f"${enterprise_value:.1f}M"]
    
    fig = go.Figure(go.Waterfall(
        name="Valuation",
        orientation="v",
        measure=waterfall_measure,
        x=waterfall_x,
        textposition="outside",
        text=waterfall_text,
        y=waterfall_y,
        connector={"line": {"color": "#64748b"}},
        increasing={"marker": {"color": "#3b82f6"}},
        totals={"marker": {"color": "#10b981"}},
        hovertemplate="<b>%{x}</b><br>Value: $%{y:.1f}M<extra></extra>"
    ))
    
    fig.update_layout(
        height=450,
        showlegend=False,
        plot_bgcolor=bg_color,
        paper_bgcolor=paper_color,
        font=dict(size=12, color=text_color),
        xaxis=dict(tickangle=-45, gridcolor=grid_color),
        yaxis=dict(gridcolor=grid_color)
    )
    
    return fig


def create_sensitivity_heatmap(
    sensitivity_matrix: np.ndarray,
    wacc_range: np.ndarray,
    tg_range: np.ndarray,
    theme: str = "light"
) -> go.Figure:
    """
    Create sensitivity analysis heatmap
    """
    bg_color = "white" if theme == "light" else "#1e293b"
    paper_color = "#f5f7fa" if theme == "light" else "#0f172a"
    text_color = "#1f2937" if theme == "light" else "#e5e7eb"
    
    fig = px.imshow(
        sensitivity_matrix,
        labels=dict(x="WACC", y="Terminal Growth Rate", color="Enterprise Value ($M)"),
        x=[f"{w:.1%}" for w in wacc_range],
        y=[f"{tg:.1%}" for tg in tg_range],
        color_continuous_scale="RdYlGn",
        aspect="auto",
        text_auto=".1f"
    )
    
    fig.update_traces(
        hovertemplate="<b>WACC:</b> %{x}<br><b>Terminal Growth:</b> %{y}<br><b>EV:</b> $%{z:.1f}M<extra></extra>"
    )
    
    fig.update_layout(
        height=400,
        font=dict(size=12, color=text_color),
        plot_bgcolor=bg_color,
        paper_bgcolor=paper_color
    )
    
    return fig

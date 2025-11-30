"""
Input Handlers
Sidebar input collection and validation
"""

import streamlit as st
from typing import Dict, List


def collect_user_inputs() -> Dict:
    """
    Collect all user inputs from sidebar
    Returns dictionary of model parameters
    """
    st.sidebar.header("Model Assumptions")
    
    # Current Revenue
    current_revenue = st.sidebar.number_input(
        "Current Annual Revenue ($M)",
        min_value=1.0,
        max_value=10000.0,
        value=100.0,
        step=5.0,
        help="Enter the company's current annual revenue in millions"
    )
    
    # Revenue Growth Rates
    st.sidebar.subheader("Revenue Growth Rates")
    growth_rates = []
    default_rates = [15.0, 12.0, 10.0, 8.0, 6.0]
    
    for year in range(1, 6):
        rate = st.sidebar.slider(
            f"Year {year} Growth Rate",
            min_value=0.0,
            max_value=30.0,
            value=default_rates[year-1],
            step=0.5,
            format="%.1f%%"
        )
        growth_rates.append(rate / 100)
    
    # Operating Assumptions
    st.sidebar.subheader("Operating Assumptions")
    
    ebit_margin = st.sidebar.slider(
        "Target EBIT Margin",
        min_value=10.0,
        max_value=40.0,
        value=20.0,
        step=1.0,
        format="%.1f%%"
    ) / 100
    
    tax_rate = st.sidebar.slider(
        "Tax Rate",
        min_value=15.0,
        max_value=35.0,
        value=25.0,
        step=1.0,
        format="%.1f%%"
    ) / 100
    
    # Valuation Parameters
    st.sidebar.subheader("Valuation Parameters")
    
    wacc = st.sidebar.slider(
        "WACC (Weighted Average Cost of Capital)",
        min_value=5.0,
        max_value=15.0,
        value=10.0,
        step=0.5,
        format="%.1f%%"
    ) / 100
    
    terminal_growth = st.sidebar.slider(
        "Terminal Growth Rate",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.25,
        format="%.2f%%"
    ) / 100
    
    fcf_conversion = st.sidebar.slider(
        "FCF Conversion Rate",
        min_value=60.0,
        max_value=100.0,
        value=80.0,
        step=5.0,
        format="%.0f%%",
        help="Percentage of NOPAT converted to Free Cash Flow"
    ) / 100
    
    return {
        'current_revenue': current_revenue,
        'growth_rates': growth_rates,
        'ebit_margin': ebit_margin,
        'tax_rate': tax_rate,
        'wacc': wacc,
        'terminal_growth': terminal_growth,
        'fcf_conversion': fcf_conversion
    }


def get_theme_toggle() -> str:
    """
    Render theme toggle in sidebar and return selected theme
    """
    st.sidebar.divider()
    theme = st.sidebar.radio(
        "Theme",
        options=["Light", "Dark"],
        index=0,
        horizontal=True
    )
    return theme.lower()

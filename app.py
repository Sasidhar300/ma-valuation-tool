"""
M&A Valuation Dashboard - Main Application
Professional DCF analysis tool for enterprise valuation
"""

import streamlit as st
import numpy as np

from models import DCFModel
from components import (
    apply_custom_css,
    render_header,
    render_metrics,
    render_insights,
    render_footer,
    create_revenue_ebit_chart,
    create_waterfall_chart,
    create_sensitivity_heatmap
)
from utils import collect_user_inputs, get_theme_toggle


# Page configuration
st.set_page_config(
    page_title="M&A Valuation Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main application logic"""
    
    # Get theme selection
    theme = get_theme_toggle()
    
    # Apply custom styling
    apply_custom_css(theme)
    
    # Render header
    render_header(theme)
    
    # Collect user inputs
    model_params = collect_user_inputs()
    
    # Initialize and run DCF model
    dcf_model = DCFModel(**model_params)
    results = dcf_model.run_valuation()
    
    # Add current revenue to results for metrics display
    results['current_revenue'] = model_params['current_revenue']
    
    # Render key metrics
    render_metrics(results, theme)
    
    st.divider()
    
    # Chart 1: Revenue & EBIT Projection
    st.subheader("Revenue & EBIT Projection")
    fig1 = create_revenue_ebit_chart(
        model_params['current_revenue'],
        results['revenues'],
        results['ebits'],
        theme
    )
    st.plotly_chart(fig1, width="stretch")
    
    # Chart 2: Valuation Waterfall
    st.subheader("Valuation Waterfall")
    fig2 = create_waterfall_chart(
        results['pv_fcfs'],
        results['pv_terminal_value'],
        results['enterprise_value'],
        theme
    )
    st.plotly_chart(fig2, width="stretch")
    
    # Chart 3: Sensitivity Analysis
    st.subheader("Sensitivity Analysis: Enterprise Value")
    
    wacc_range = np.linspace(0.06, 0.14, 9)
    tg_range = np.linspace(0.02, 0.05, 7)
    
    sensitivity_matrix = dcf_model.sensitivity_analysis(wacc_range, tg_range)
    
    fig3 = create_sensitivity_heatmap(sensitivity_matrix, wacc_range, tg_range, theme)
    st.plotly_chart(fig3, width="stretch")
    
    # Render insights
    render_insights(results, model_params, theme)
    
    # Render footer
    render_footer()


if __name__ == "__main__":
    main()

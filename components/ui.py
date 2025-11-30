"""
UI Components
Reusable UI elements and styling for the dashboard
"""

import streamlit as st
from typing import Dict


def apply_custom_css(theme: str = "light"):
    """Apply custom CSS styling based on theme"""
    
    if theme == "light":
        bg_color = "#f5f7fa"
        text_color = "#1f2937"
        card_bg = "white"
        header_color = "#1e3a8a"
        subheader_color = "#1e40af"
        secondary_text = "#4b5563"
    else:
        bg_color = "#0f172a"
        text_color = "#e5e7eb"
        card_bg = "#1e293b"
        header_color = "#60a5fa"
        subheader_color = "#3b82f6"
        secondary_text = "#9ca3af"
    
    st.markdown(f"""
        <style>
        /* Main background */
        .main {{
            background-color: {bg_color};
        }}
        
        /* Metric cards */
        .stMetric {{
            background-color: {card_bg};
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Headers */
        h1 {{
            color: {header_color} !important;
            font-weight: 700;
        }}
        h2 {{
            color: {subheader_color} !important;
            font-weight: 600;
            margin-top: 2rem;
        }}
        h3 {{
            color: {subheader_color} !important;
            font-weight: 500;
        }}
        
        /* Sliders */
        .stSlider {{
            padding: 10px 0;
        }}
        
        /* Markdown content - be specific to avoid breaking other elements */
        .stMarkdown {{
            color: {text_color};
        }}
        .stMarkdown p {{
            color: {text_color} !important;
        }}
        .stMarkdown li {{
            color: {text_color} !important;
        }}
        .stMarkdown strong {{
            color: {text_color} !important;
        }}
        
        /* Captions */
        .stCaptionContainer {{
            color: {secondary_text} !important;
        }}
        
        /* Metric text */
        [data-testid="stMetricLabel"] {{
            color: {text_color} !important;
        }}
        [data-testid="stMetricValue"] {{
            color: {text_color} !important;
        }}
        [data-testid="stMetricDelta"] {{
            color: {text_color} !important;
        }}
        
        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {card_bg};
        }}
        [data-testid="stSidebar"] label {{
            color: {text_color} !important;
        }}
        [data-testid="stSidebar"] p {{
            color: {text_color} !important;
        }}
        
        /* Warning and error boxes */
        .stAlert {{
            color: {text_color} !important;
        }}
        </style>
        """, unsafe_allow_html=True)


def render_header(theme: str = "light"):
    """Render dashboard header"""
    st.title("M&A Valuation Dashboard")
    st.markdown("**Professional DCF Analysis Tool** | Enterprise Valuation & Sensitivity Analysis")
    st.divider()


def render_metrics(results: Dict, theme: str = "light"):
    """Render key metrics display"""
    st.subheader("Valuation Summary")
    
    col1, col2, col3 = st.columns(3)
    
    current_revenue = results.get('current_revenue', 100)
    enterprise_value = results['enterprise_value']
    pv_forecast_period = results['pv_forecast_period']
    pv_terminal_value = results['pv_terminal_value']
    
    with col1:
        st.metric(
            label="Enterprise Value",
            value=f"${enterprise_value:.1f}M",
            delta=f"{(enterprise_value / current_revenue):.1f}x Revenue Multiple"
        )
    
    with col2:
        st.metric(
            label="PV of Cash Flows (Years 1-5)",
            value=f"${pv_forecast_period:.1f}M",
            delta=f"{(pv_forecast_period / enterprise_value * 100):.1f}% of Total"
        )
    
    with col3:
        st.metric(
            label="PV of Terminal Value",
            value=f"${pv_terminal_value:.1f}M",
            delta=f"{(pv_terminal_value / enterprise_value * 100):.1f}% of Total"
        )


def render_insights(results: Dict, model_params: Dict, theme: str = "light"):
    """Render key insights section"""
    st.divider()
    st.subheader("Key Insights")
    
    col_left, col_right = st.columns(2)
    
    enterprise_value = results['enterprise_value']
    pv_terminal_value = results['pv_terminal_value']
    pv_forecast_period = results['pv_forecast_period']
    projected_revenues = results['revenues']
    ebits = results['ebits']
    
    current_revenue = model_params['current_revenue']
    growth_rates = model_params['growth_rates']
    terminal_growth = model_params['terminal_growth']
    tax_rate = model_params['tax_rate']
    wacc = model_params['wacc']
    
    with col_left:
        st.markdown("### Valuation Summary")
        st.markdown(f"""
        - **Enterprise Value**: ${enterprise_value:.1f}M
        - **Revenue Multiple**: {(enterprise_value / projected_revenues[-1]):.2f}x (EV / Year 5 Revenue)
        - **EBITDA Multiple**: {(enterprise_value / (ebits[-1] * (1/(1-tax_rate)))):.2f}x (estimated)
        - **Terminal Value Contribution**: {(pv_terminal_value / enterprise_value * 100):.1f}%
        - **Forecast Period Contribution**: {(pv_forecast_period / enterprise_value * 100):.1f}%
        """)
        
        cagr = ((projected_revenues[-1] / current_revenue) ** (1/5) - 1)
        st.markdown(f"""
        **Growth Profile**:
        - Initial Growth: {growth_rates[0]:.1%} → {growth_rates[-1]:.1%}
        - Terminal Growth: {terminal_growth:.2%}
        - CAGR (5Y): {cagr:.2%}
        """)
    
    with col_right:
        st.markdown("### Risk Factors & Assumptions")
        
        # Calculate WACC sensitivity
        from models.dcf_model import DCFModel
        model = DCFModel(**model_params)
        wacc_sensitivity, _ = model.calculate_wacc_sensitivity()
        
        st.markdown(f"""
        - **WACC Sensitivity**: ±1% change in WACC = ±{wacc_sensitivity*100:.1f}% change in EV
        - **Terminal Value Dependency**: {(pv_terminal_value / enterprise_value * 100):.1f}% of value in terminal period
        - **FCF Conversion Assumption**: {model_params['fcf_conversion']:.0%} of NOPAT
        - **Key Assumption**: EBIT margin held constant at {model_params['ebit_margin']:.1%}
        """)
        
        if pv_terminal_value / enterprise_value > 0.75:
            st.warning("**High Terminal Value Risk**: >75% of value in terminal period increases uncertainty")
        
        if wacc - terminal_growth < 0.03:
            st.error("**Model Warning**: WACC-Terminal Growth spread <3% may produce unreliable results")


def render_footer():
    """Render dashboard footer"""
    st.divider()
    st.caption("Built for M&A Analysis | Professional DCF Valuation Tool")
    st.caption("For illustrative purposes only. Consult financial professionals for investment decisions.")

"""
M&A Valuation Dashboard - DCF Analysis Tool
Professional-grade discounted cash flow valuation tool for M&A analysis
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page configuration
st.set_page_config(
    page_title="M&A Valuation Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main {
        background-color: #f5f7fa;
    }
    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }
    h2 {
        color: #1e40af;
        font-weight: 600;
        margin-top: 2rem;
    }
    h3 {
        color: #3b82f6;
        font-weight: 500;
    }
    .stSlider {
        padding: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Header
st.title("M&A Valuation Dashboard")
st.markdown("**Professional DCF Analysis Tool** | Enterprise Valuation & Sensitivity Analysis")
st.divider()

# ==================== SIDEBAR: USER INPUTS ====================
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

st.sidebar.subheader("Revenue Growth Rates")
growth_rates = []
for year in range(1, 6):
    rate = st.sidebar.slider(
        f"Year {year} Growth Rate",
        min_value=0.0,
        max_value=30.0,
        value=[15.0, 12.0, 10.0, 8.0, 6.0][year-1],
        step=0.5,
        format="%.1f%%"
    )
    growth_rates.append(rate / 100)

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

# ==================== DCF CALCULATIONS ====================

# Project 5-year revenue
revenues = [current_revenue]
for i, growth in enumerate(growth_rates):
    revenues.append(revenues[-1] * (1 + growth))

# Remove year 0 for projections (keep only years 1-5)
projected_revenues = revenues[1:]

# Calculate EBIT for each year
ebits = [rev * ebit_margin for rev in projected_revenues]

# Calculate NOPAT (Net Operating Profit After Tax)
nopats = [ebit * (1 - tax_rate) for ebit in ebits]

# Calculate Free Cash Flow
fcfs = [nopat * fcf_conversion for nopat in nopats]

# Calculate discount factors
discount_factors = [(1 / (1 + wacc) ** year) for year in range(1, 6)]

# Calculate present value of each year's FCF
pv_fcfs = [fcf * df for fcf, df in zip(fcfs, discount_factors)]

# Calculate Terminal Value
terminal_value = fcfs[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
pv_terminal_value = terminal_value * discount_factors[-1]

# Calculate Enterprise Value
pv_forecast_period = sum(pv_fcfs)
enterprise_value = pv_forecast_period + pv_terminal_value

# ==================== KEY METRICS DISPLAY ====================

st.subheader("Valuation Summary")

col1, col2, col3 = st.columns(3)

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

st.divider()

# ==================== CHART 1: REVENUE & EBIT PROJECTION ====================

st.subheader("Revenue & EBIT Projection")

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

# Add Revenue bars
fig1.add_trace(
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
fig1.add_trace(
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
fig1.update_xaxes(title_text="Year")
fig1.update_yaxes(title_text="Revenue ($M)", secondary_y=False)
fig1.update_yaxes(title_text="EBIT ($M)", secondary_y=True)

fig1.update_layout(
    height=450,
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=12)
)

st.plotly_chart(fig1, width="stretch")

# ==================== CHART 2: VALUATION WATERFALL ====================

st.subheader("Valuation Waterfall")

# Prepare waterfall data
waterfall_measure = ["relative"] * 5 + ["relative", "total"]
waterfall_x = [f"Year {i} FCF" for i in range(1, 6)] + ["Terminal Value", "Enterprise Value"]
waterfall_y = pv_fcfs + [pv_terminal_value, 0]  # 0 for total (will show cumulative)
waterfall_text = [f"${val:.1f}M" for val in pv_fcfs] + [f"${pv_terminal_value:.1f}M", f"${enterprise_value:.1f}M"]

fig2 = go.Figure(go.Waterfall(
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

fig2.update_layout(
    height=450,
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(size=12),
    xaxis=dict(tickangle=-45)
)

st.plotly_chart(fig2, width="stretch")

# ==================== CHART 3: SENSITIVITY ANALYSIS ====================

st.subheader("Sensitivity Analysis: Enterprise Value")

# Create sensitivity matrix
wacc_range = np.linspace(0.06, 0.14, 9)
tg_range = np.linspace(0.02, 0.05, 7)

sensitivity_matrix = np.zeros((len(tg_range), len(wacc_range)))

for i, tg in enumerate(tg_range):
    for j, w in enumerate(wacc_range):
        # Recalculate with different WACC and terminal growth
        temp_discount_factors = [(1 / (1 + w) ** year) for year in range(1, 6)]
        temp_pv_fcfs = [fcf * df for fcf, df in zip(fcfs, temp_discount_factors)]
        temp_terminal_value = fcfs[-1] * (1 + tg) / (w - tg)
        temp_pv_terminal = temp_terminal_value * temp_discount_factors[-1]
        sensitivity_matrix[i, j] = sum(temp_pv_fcfs) + temp_pv_terminal

# Create heatmap
fig3 = px.imshow(
    sensitivity_matrix,
    labels=dict(x="WACC", y="Terminal Growth Rate", color="Enterprise Value ($M)"),
    x=[f"{w:.1%}" for w in wacc_range],
    y=[f"{tg:.1%}" for tg in tg_range],
    color_continuous_scale="RdYlGn",
    aspect="auto",
    text_auto=".1f"
)

fig3.update_traces(
    hovertemplate="<b>WACC:</b> %{x}<br><b>Terminal Growth:</b> %{y}<br><b>EV:</b> $%{z:.1f}M<extra></extra>"
)

fig3.update_layout(
    height=400,
    font=dict(size=12),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig3, width="stretch")

# ==================== KEY INSIGHTS SECTION ====================

st.divider()
st.subheader("Key Insights")

col_left, col_right = st.columns(2)

with col_left:
    st.markdown("### Valuation Summary")
    st.markdown(f"""
    - **Enterprise Value**: ${enterprise_value:.1f}M
    - **Revenue Multiple**: {(enterprise_value / projected_revenues[-1]):.2f}x (EV / Year 5 Revenue)
    - **EBITDA Multiple**: {(enterprise_value / (ebits[-1] * (1/(1-tax_rate)))):.2f}x (estimated)
    - **Terminal Value Contribution**: {(pv_terminal_value / enterprise_value * 100):.1f}%
    - **Forecast Period Contribution**: {(pv_forecast_period / enterprise_value * 100):.1f}%
    """)
    
    st.markdown(f"""
    **Growth Profile**:
    - Initial Growth: {growth_rates[0]:.1%} → {growth_rates[-1]:.1%}
    - Terminal Growth: {terminal_growth:.2%}
    - CAGR (5Y): {((projected_revenues[-1] / current_revenue) ** (1/5) - 1):.2%}
    """)

with col_right:
    st.markdown("### Risk Factors & Assumptions")
    
    # Calculate sensitivity metrics
    ev_at_wacc_plus_1 = sum([fcf * (1 / (1 + wacc + 0.01) ** (i+1)) for i, fcf in enumerate(fcfs)]) + \
                         (fcfs[-1] * (1 + terminal_growth) / (wacc + 0.01 - terminal_growth)) * (1 / (1 + wacc + 0.01) ** 5)
    ev_at_wacc_minus_1 = sum([fcf * (1 / (1 + wacc - 0.01) ** (i+1)) for i, fcf in enumerate(fcfs)]) + \
                          (fcfs[-1] * (1 + terminal_growth) / (wacc - 0.01 - terminal_growth)) * (1 / (1 + wacc - 0.01) ** 5)
    
    wacc_sensitivity = (ev_at_wacc_minus_1 - ev_at_wacc_plus_1) / (2 * enterprise_value)
    
    st.markdown(f"""
    - **WACC Sensitivity**: ±1% change in WACC = ±{wacc_sensitivity*100:.1f}% change in EV
    - **Terminal Value Dependency**: {(pv_terminal_value / enterprise_value * 100):.1f}% of value in terminal period
    - **FCF Conversion Assumption**: {fcf_conversion:.0%} of NOPAT
    - **Key Assumption**: EBIT margin held constant at {ebit_margin:.1%}
    """)
    
    if pv_terminal_value / enterprise_value > 0.75:
        st.warning("**High Terminal Value Risk**: >75% of value in terminal period increases uncertainty")
    
    if wacc - terminal_growth < 0.03:
        st.error("**Model Warning**: WACC-Terminal Growth spread <3% may produce unreliable results")

# Footer
st.divider()
st.caption("Built for M&A Analysis | Professional DCF Valuation Tool")
st.caption("For illustrative purposes only. Consult financial professionals for investment decisions.")

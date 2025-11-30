# DCF Valuation Dashboard

Professional M&A valuation tool built with Streamlit and Plotly. Features interactive DCF modeling, sensitivity analysis, and light/dark themes.

## Features

- **DCF Valuation Model**: 5-year projections with customizable assumptions
- **Interactive Charts**: Revenue/EBIT trends, valuation waterfall, sensitivity heatmap
- **Sensitivity Analysis**: WACC vs Terminal Growth matrix (63 scenarios)
- **Theme Support**: Light and dark modes
- **Modular Architecture**: Clean separation of models, components, and utilities

## Quick Start

```bash
# Clone repository
git clone https://github.com/Sasidhar300/ma-valuation-tool.git
cd ma-valuation-tool

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## Project Structure

```
dcf-valuation-dashboard/
├── app.py                      # Main application
├── models/
│   └── dcf_model.py           # DCF calculations
├── components/
│   ├── charts.py              # Plotly visualizations
│   └── ui.py                  # UI components
├── utils/
│   └── inputs.py              # Input handlers
├── requirements.txt
└── README.md
```

## Usage

1. Adjust model assumptions in the sidebar
2. View real-time valuation updates
3. Analyze sensitivity to key parameters
4. Toggle between light/dark themes

## Technologies

- Python 3.10+
- Streamlit
- Plotly
- Pandas & NumPy

## License

MIT License

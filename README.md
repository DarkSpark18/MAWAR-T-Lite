# MAWAR T LITE

<div align="center">

![Logo](assets/images/logo.png)

**Multi-metrix Analytics for Wealth, Assets & Risk**

*A Bloomberg Terminal-inspired stock market analytics platform*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Deploy](https://img.shields.io/badge/Deploy-Streamlit-Cloud-FF9900.svg)](https://streamlit.io/cloud)

</div>

---

## 🚀 Live Demo

**Try it now on Streamlit Cloud**: [MAWAR T Lite](https://share.streamlit.io/)

*No installation required - runs directly in your browser!*

---

## ✨ Features

### 📊 Market Dashboard
- Real-time data for **Top 50 Global Stocks**
- Pin your favorite stocks for quick access
- Comprehensive stock details with interactive charts
- Search and filter capabilities

### 💼 Portfolio Manager
- Track unlimited investment positions
- Real-time P&L calculations
- Visual allocation breakdown
- Export portfolio to CSV

### 🎲 Monte Carlo Predictor
- Statistical price simulations
- Configurable parameters (days, simulations, confidence)
- Interactive visualization of price paths
- Risk metrics (Value at Risk)

---

## 🎨 Design

Bloomberg Terminal-inspired dark theme featuring:

| Element | Style |
|---------|-------|
| **Font** | JetBrains Mono (monospace) |
| **Primary Color** | Orange (#FF9900) |
| **Gains** | Green (#00FF00) |
| **Losses** | Red (#FF0000) |
| **Background** | Pure Black (#000000) |
| **Panels** | Dark Gray (#1A1A1A) |

---

## 🛠️ Quick Start

### Run Locally

```bash
# Clone the repository
git clone https://github.com/yourusername/mawar-t-lite.git
cd mawar-t-lite

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py

# Open http://localhost:8501
```

### Deploy to Streamlit Cloud

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io/)
3. Click "Deploy an app"
4. Select your forked repository
5. Set main file path to `app.py`
6. Click **Deploy!**

---

## 📁 Project Structure

```
mawar-t-lite/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
├── pyproject.toml          # Project metadata
│
├── config/                 # Configuration
│   ├── settings.py         # App settings
│   ├── theme.py            # Bloomberg-style theme
│   └── stocks_list.py      # Top 50 stocks
│
├── modules/                 # Core features
│   ├── dashboard.py        # Market dashboard
│   ├── portfolio.py        # Portfolio manager
│   ├── predictor.py        # Monte Carlo
│   └── data_fetcher.py     # yfinance wrapper
│
├── utils/                  # Utilities
│   ├── calculations.py     # Financial math
│   ├── charts.py           # Plotly charts
│   ├── storage.py          # JSON persistence
│   └── validators.py       # Input validation
│
├── components/             # UI components
│   ├── header.py
│   ├── metric_card.py
│   ├── stock_card.py
│   └── data_table.py
│
├── data/                   # Local storage
│   ├── portfolio.json
│   └── pinned_stocks.json
│
├── assets/
│   └── images/
│       ├── logo.png
│       └── favicon.ico
│
└── tests/                  # Unit tests (38 tests)
```

---

## 📊 Data Sources

**Provider**: Yahoo Finance (via `yfinance`)

- Real-time stock prices
- Historical data (up to 10 years)
- Company information & ratios
- Volume data

> **Note**: Data has 15-20 minute delay. Not suitable for high-frequency trading.

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_calculations.py -v
```

**Test Results**: 38 tests passing ✅

---

## 🔧 Configuration

Edit `config/settings.py` to customize:

```python
CACHE_TTL = 60              # Cache duration (seconds)
MAX_PINNED_STOCKS = 5       # Maximum pinned stocks
DEFAULT_SIMULATIONS = 5000  # Monte Carlo simulations
DEFAULT_CONFIDENCE = 95     # Confidence level (%)
```

---

## 📜 License

MIT License - see [LICENSE](LICENSE) for details.

---

## ⚠️ Disclaimer

**FOR EDUCATIONAL PURPOSES ONLY**

- Not financial advice
- Not investment recommendations
- Past performance does not guarantee future results
- Always do your own research

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Web framework
- [yfinance](https://github.com/ranaroussi/yfinance) - Stock data
- [Plotly](https://plotly.com/) - Interactive charts
- [Bloomberg Terminal](https://www.bloomberg.com/) - Design inspiration

---

<div align="center">

**Built with ❤️ using Python & Streamlit**

*Star this repo if you find it useful!* ⭐

</div>

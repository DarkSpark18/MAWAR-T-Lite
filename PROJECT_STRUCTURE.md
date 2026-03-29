# MAWAR T LITE - PROJECT STRUCTURE

```
mawar-t-lite/
│
├── 📄 app.py                          # Main Streamlit application entry point
├── 📄 requirements.txt                # Python dependencies
├── 📄 README.md                       # Project documentation & setup guide
├── 📄 PROJECT_OVERVIEW.md            # Comprehensive project overview
├── 📄 TECHNICAL_SPEC.md              # Detailed technical specifications
├── 📄 .gitignore                      # Git ignore file
├── 📄 LICENSE                         # MIT License
│
├── 📁 config/                         # Configuration files
│   ├── 📄 __init__.py
│   ├── 📄 settings.py                # App configuration (API keys, constants)
│   ├── 📄 theme.py                   # Bloomberg-style theme colors & fonts
│   └── 📄 stocks_list.py             # Top 50 global stocks list
│
├── 📁 data/                           # Persistent data storage
│   ├── 📄 .gitkeep                   # Keep directory in git
│   ├── 📄 portfolio.json             # User portfolio positions
│   ├── 📄 pinned_stocks.json         # Pinned stocks data
│   └── 📁 cache/                      # Cache directory for stock data
│       └── 📄 .gitkeep
│
├── 📁 modules/                        # Core application modules
│   ├── 📄 __init__.py
│   │
│   ├── 📄 dashboard.py               # Market Dashboard page
│   │   ├── display_top_stocks()
│   │   ├── display_pinned_stocks()
│   │   ├── stock_details_modal()
│   │   └── handle_pin_unpin()
│   │
│   ├── 📄 portfolio.py               # Portfolio Management page
│   │   ├── display_portfolio_summary()
│   │   ├── display_positions_table()
│   │   ├── add_position_form()
│   │   ├── edit_position_form()
│   │   ├── delete_position()
│   │   ├── calculate_portfolio_metrics()
│   │   └── export_portfolio()
│   │
│   ├── 📄 predictor.py               # Monte Carlo Predictor page
│   │   ├── stock_selection_ui()
│   │   ├── simulation_parameters_ui()
│   │   ├── run_monte_carlo()
│   │   ├── display_simulation_results()
│   │   └── generate_charts()
│   │
│   └── 📄 data_fetcher.py            # Stock data fetching utilities
│       ├── fetch_stock_info()
│       ├── fetch_historical_data()
│       ├── fetch_multiple_stocks()
│       ├── validate_ticker()
│       └── search_stocks()
│
├── 📁 utils/                          # Utility functions
│   ├── 📄 __init__.py
│   │
│   ├── 📄 calculations.py            # Financial calculations
│   │   ├── calculate_return()
│   │   ├── calculate_sharpe_ratio()
│   │   ├── calculate_volatility()
│   │   └── format_currency()
│   │
│   ├── 📄 storage.py                 # Data persistence utilities
│   │   ├── save_portfolio()
│   │   ├── load_portfolio()
│   │   ├── save_pinned_stocks()
│   │   ├── load_pinned_stocks()
│   │   └── export_to_csv()
│   │
│   ├── 📄 validators.py              # Input validation
│   │   ├── validate_ticker_symbol()
│   │   ├── validate_quantity()
│   │   ├── validate_price()
│   │   └── validate_date()
│   │
│   └── 📄 charts.py                  # Chart generation utilities
│       ├── create_price_chart()
│       ├── create_portfolio_allocation()
│       ├── create_performance_timeline()
│       └── create_monte_carlo_chart()
│
├── 📁 components/                     # Reusable UI components
│   ├── 📄 __init__.py
│   ├── 📄 header.py                  # Terminal header component
│   ├── 📄 stock_card.py              # Stock display card
│   ├── 📄 metric_card.py             # Metric display card
│   └── 📄 data_table.py              # Enhanced data table component
│
├── 📁 assets/                         # Static assets
│   ├── 📁 css/
│   │   └── 📄 custom_styles.css      # Additional custom CSS
│   ├── 📁 images/
│   │   ├── 📄 logo.png               # Application logo
│   │   └── 📄 favicon.ico            # Browser favicon
│   └── 📁 fonts/
│       └── 📄 .gitkeep
│
├── 📁 tests/                          # Test files
│   ├── 📄 __init__.py
│   ├── 📄 test_calculations.py
│   ├── 📄 test_data_fetcher.py
│   ├── 📄 test_portfolio.py
│   └── 📄 test_predictor.py
│
└── 📁 docs/                           # Additional documentation
    ├── 📄 USER_GUIDE.md              # End-user documentation
    ├── 📄 API_REFERENCE.md           # Function reference
    ├── 📄 DEPLOYMENT.md              # Deployment instructions
    └── 📁 screenshots/               # Application screenshots
        └── 📄 .gitkeep
```

## 📝 File Descriptions

### Root Files

- **app.py**: Main entry point. Handles page routing, navigation, and renders the appropriate module based on user selection.

- **requirements.txt**: Lists all Python package dependencies with version specifications.

- **README.md**: Primary documentation including setup instructions, features overview, and quick start guide.

### Config Directory

- **settings.py**: Central configuration including app title, refresh rates, API endpoints, and feature flags.

- **theme.py**: Bloomberg-style theme definition with color palette, typography, and CSS variables.

- **stocks_list.py**: Curated list of top 50 global stocks with metadata (symbol, name, sector, market).

### Data Directory

- **portfolio.json**: Stores user's portfolio positions in JSON format.

- **pinned_stocks.json**: Stores user's pinned stocks preferences.

- **cache/**: Temporary cache for stock data to reduce API calls.

### Modules Directory

- **dashboard.py**: Implements the market dashboard with stock listings, details view, and pinning functionality.

- **portfolio.py**: Implements portfolio management features including CRUD operations and analytics.

- **predictor.py**: Implements Monte Carlo simulation engine and visualization.

- **data_fetcher.py**: Centralized module for all stock data fetching operations using yfinance.

### Utils Directory

- **calculations.py**: Pure functions for financial calculations (returns, ratios, statistics).

- **storage.py**: Handles all file I/O operations for data persistence.

- **validators.py**: Input validation functions for user data.

- **charts.py**: Plotly chart generation functions for various visualizations.

### Components Directory

- **header.py**: Reusable terminal header with branding.

- **stock_card.py**: Styled stock information card component.

- **metric_card.py**: Metric display card with optional sparklines.

- **data_table.py**: Enhanced table component with sorting, filtering, and pagination.

### Assets Directory

- **css/**: Additional CSS files for advanced styling.

- **images/**: Logo, favicon, and other image assets.

- **fonts/**: Custom web fonts if needed.

### Tests Directory

- Unit tests for all major functions and modules.

### Docs Directory

- Comprehensive documentation for users and developers.

---

## 🔄 Data Flow

```
User Input (Streamlit UI)
    ↓
app.py (Router)
    ↓
Module (dashboard/portfolio/predictor)
    ↓
Utils/Data Fetcher
    ↓
yfinance API / Local Storage
    ↓
Data Processing
    ↓
Charts/Tables Generation
    ↓
Display to User
```

---

## 🚀 Development Workflow

1. **Setup**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Development Server**
   ```bash
   streamlit run app.py
   ```

3. **Access Application**
   ```
   http://localhost:8501
   ```

4. **Make Changes**
   - Edit files
   - Streamlit auto-reloads
   - Test in browser

5. **Testing**
   ```bash
   pytest tests/
   ```

---

## 📦 Module Dependencies

```
app.py
├── modules/dashboard.py
│   ├── utils/storage.py
│   ├── utils/validators.py
│   ├── modules/data_fetcher.py
│   └── components/stock_card.py
│
├── modules/portfolio.py
│   ├── utils/storage.py
│   ├── utils/calculations.py
│   ├── utils/charts.py
│   ├── modules/data_fetcher.py
│   └── components/metric_card.py
│
└── modules/predictor.py
    ├── modules/data_fetcher.py
    ├── utils/charts.py
    └── utils/calculations.py
```

---

## 🎯 Implementation Priority

### Phase 1 (Week 1)
1. Setup project structure ✓
2. Create config files
3. Implement data_fetcher module
4. Build basic dashboard

### Phase 2 (Week 2)
5. Implement pinned stocks feature
6. Add stock details modal
7. Create portfolio module basics

### Phase 3 (Week 3)
8. Complete portfolio analytics
9. Add portfolio charts
10. Implement data persistence

### Phase 4 (Week 4)
11. Build Monte Carlo simulator
12. Add prediction visualizations
13. Finalize styling

### Phase 5 (Week 5)
14. Testing and bug fixes
15. Documentation
16. Performance optimization

---

**Document Version**: 1.0
**Last Updated**: March 29, 2026
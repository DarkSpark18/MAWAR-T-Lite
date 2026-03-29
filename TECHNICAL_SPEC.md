# MAWAR T LITE - TECHNICAL SPECIFICATION

## 📐 SYSTEM ARCHITECTURE

### High-Level Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   STREAMLIT UI LAYER                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │  Dashboard   │ │  Portfolio   │ │  Predictor   │   │
│  │     Page     │ │     Page     │ │     Page     │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                   BUSINESS LOGIC LAYER                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │   Market     │ │  Portfolio   │ │ Monte Carlo  │   │
│  │   Handler    │ │   Manager    │ │  Simulator   │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│                    DATA ACCESS LAYER                    │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐   │
│  │   yfinance   │ │     JSON     │ │   Session    │   │
│  │     API      │ │   Storage    │ │    State     │   │
│  └──────────────┘ └──────────────┘ └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 FEATURE SPECIFICATIONS

### 1. MARKET DASHBOARD

#### 1.1 Top 50 Global Stocks Display

**Data Structure:**
```python
{
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "price": 178.25,
    "change": 2.45,
    "change_percent": 1.39,
    "market_cap": 2800000000000,
    "volume": 58432100,
    "pe_ratio": 28.5,
    "week_52_high": 199.62,
    "week_52_low": 124.17,
    "avg_volume": 52000000,
    "beta": 1.25,
    "dividend_yield": 0.52,
    "sector": "Technology",
    "industry": "Consumer Electronics"
}
```

**Functionality:**
- Fetch real-time data on page load
- Auto-refresh every 60 seconds (configurable)
- Sort by: Price, Change %, Market Cap, Volume, P/E
- Filter by: Sector, Price Range, Market Cap
- Search by ticker or company name

**Display:**
- Table view with sortable columns
- Color-coded change indicators (green/red)
- Responsive grid layout
- Pagination (10/25/50 per page)

#### 1.2 Stock Details Modal

**Triggered By:** Click on any stock row

**Displays:**
- **Header Section:**
  - Company name and logo (if available)
  - Current price (large, prominent)
  - Day change and %
  - Timestamp of last update

- **Chart Section:**
  - Interactive price chart
  - Timeframe selector: 1D, 5D, 1M, 3M, 6M, 1Y, 5Y, MAX
  - Volume bars below price
  - Technical indicators toggle

- **Statistics Section:**
  ```
  ┌─────────────────┬─────────────────┐
  │ Previous Close  │ $176.80         │
  │ Open            │ $177.50         │
  │ Day Range       │ $176.50-$178.90 │
  │ 52 Week Range   │ $124.17-$199.62 │
  │ Volume          │ 58.4M           │
  │ Avg Volume      │ 52.0M           │
  │ Market Cap      │ $2.80T          │
  │ Beta (5Y)       │ 1.25            │
  │ PE Ratio (TTM)  │ 28.5            │
  │ EPS (TTM)       │ $6.25           │
  │ Div Yield       │ 0.52%           │
  └─────────────────┴─────────────────┘
  ```

- **Action Buttons:**
  - Pin/Unpin Stock
  - Add to Portfolio
  - View Full Analysis
  - Export Data

#### 1.3 Pinned Stocks Feature

**Requirements:**
- Maximum 5 pinned stocks
- Persistent across sessions
- Displayed at top of dashboard
- Drag-and-drop reordering
- Quick unpin option

**Storage Format (JSON):**
```json
{
  "pinned_stocks": [
    {
      "symbol": "AAPL",
      "pinned_at": "2026-03-29T10:30:00",
      "order": 1
    },
    {
      "symbol": "GOOGL",
      "pinned_at": "2026-03-29T10:31:00",
      "order": 2
    }
  ]
}
```

**UI Behavior:**
- Show "PINNED" badge
- Orange border highlighting
- Pin icon changes to filled state
- Warning when trying to pin 6th stock

---

### 2. PORTFOLIO MANAGER

#### 2.1 Data Model

**Portfolio Position:**
```python
{
    "id": "uuid-string",
    "symbol": "AAPL",
    "name": "Apple Inc.",
    "quantity": 10.0,
    "purchase_price": 150.00,
    "purchase_date": "2025-01-15",
    "current_price": 178.25,  # Fetched in real-time
    "cost_basis": 1500.00,    # quantity * purchase_price
    "current_value": 1782.50,  # quantity * current_price
    "gain_loss": 282.50,       # current_value - cost_basis
    "gain_loss_percent": 18.83,
    "notes": "Long-term hold",
    "created_at": "2025-01-15T14:30:00",
    "updated_at": "2026-03-29T10:30:00"
}
```

**Portfolio Summary:**
```python
{
    "total_positions": 15,
    "total_cost_basis": 50000.00,
    "total_current_value": 62500.00,
    "total_gain_loss": 12500.00,
    "total_gain_loss_percent": 25.00,
    "best_performer": {
        "symbol": "NVDA",
        "gain_percent": 125.5
    },
    "worst_performer": {
        "symbol": "META",
        "gain_percent": -5.2
    },
    "last_updated": "2026-03-29T10:30:00"
}
```

#### 2.2 Functionality

**Add Position:**
- Form fields:
  - Stock ticker (with autocomplete)
  - Quantity (float, min 0.001)
  - Purchase price (float, min 0.01)
  - Purchase date (date picker)
  - Notes (optional, max 500 chars)
- Validation:
  - Ticker exists and is valid
  - Positive values only
  - Date not in future
- Auto-fetch current price on add

**Edit Position:**
- Update quantity, price, date, notes
- Recalculate all metrics
- Log change history

**Delete Position:**
- Confirmation dialog
- Soft delete with archive option
- Update portfolio summary

**Bulk Actions:**
- Select multiple positions
- Delete selected
- Export selected to CSV

#### 2.3 Analytics Dashboard

**Top Metrics Cards:**
```
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ TOTAL VALUE         │ │ TOTAL GAIN/LOSS     │ │ TODAY'S CHANGE      │
│ $62,500.00          │ │ +$12,500.00         │ │ +$850.50            │
│ 💰                  │ │ +25.00% 📈          │ │ +1.38% 🟢          │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘

┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│ POSITIONS           │ │ BEST PERFORMER      │ │ WORST PERFORMER     │
│ 15                  │ │ NVDA                │ │ META                │
│ 📊                  │ │ +125.5% 🚀         │ │ -5.2% 📉           │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘
```

**Charts:**
1. **Allocation Pie Chart**
   - By stock (% of portfolio)
   - Color-coded by sector
   - Interactive hover details

2. **Performance Timeline**
   - Portfolio value over time
   - Cost basis line for reference
   - Gain/loss area fill

3. **Position Comparison Bar Chart**
   - All positions ranked by gain/loss %
   - Color gradient: red → yellow → green

**Positions Table:**
```
┌────────┬──────────────┬──────┬─────────┬─────────┬───────────┬──────────┬──────────┐
│ Symbol │ Name         │ Qty  │ Avg Cost│ Current │ Value     │ Gain/Loss│ Return % │
├────────┼──────────────┼──────┼─────────┼─────────┼───────────┼──────────┼──────────┤
│ AAPL   │ Apple Inc.   │ 10.0 │ $150.00 │ $178.25 │ $1,782.50 │ +$282.50 │ +18.83%  │
│ GOOGL  │ Alphabet Inc.│ 5.0  │ $120.00 │ $135.50 │ $677.50   │ +$77.50  │ +12.92%  │
│ ...    │ ...          │ ...  │ ...     │ ...     │ ...       │ ...      │ ...      │
└────────┴──────────────┴──────┴─────────┴─────────┴───────────┴──────────┴──────────┘
```

#### 2.4 Export Options

**CSV Export Format:**
```csv
Symbol,Name,Quantity,Purchase_Price,Purchase_Date,Current_Price,Current_Value,Cost_Basis,Gain_Loss,Gain_Loss_Percent
AAPL,Apple Inc.,10.0,150.00,2025-01-15,178.25,1782.50,1500.00,282.50,18.83
```

**PDF Report:** (Future enhancement)
- Summary page
- Detailed positions
- Charts and graphs
- Generated with timestamp

---

### 3. MONTE CARLO PREDICTOR

#### 3.1 Input Parameters

**Stock Selection:**
- Search box with autocomplete
- Display current price and company name
- Show 30-day historical mini-chart

**Simulation Settings:**
```python
{
    "prediction_days": [30, 60, 90, 180, 365],  # Dropdown options
    "num_simulations": [1000, 5000, 10000],     # Dropdown options
    "confidence_level": [68, 95, 99],           # Confidence intervals
    "selected_days": 30,                         # Default
    "selected_simulations": 5000,                # Default
    "selected_confidence": 95                    # Default
}
```

**Advanced Options (Collapsible):**
- Use historical volatility vs custom volatility
- Include dividends in simulation
- Risk-free rate assumption
- Mean return override

#### 3.2 Monte Carlo Algorithm

**Mathematical Foundation:**

1. **Calculate Historical Metrics:**
   ```python
   # Get historical data
   daily_returns = (prices / prices.shift(1)) - 1
   
   # Calculate parameters
   mean_return = daily_returns.mean()
   std_deviation = daily_returns.std()
   drift = mean_return - (0.5 * std_deviation ** 2)
   ```

2. **Simulate Price Paths:**
   ```python
   for simulation in range(num_simulations):
       prices = [current_price]
       for day in range(prediction_days):
           # Geometric Brownian Motion
           shock = np.random.normal(0, std_deviation)
           price = prices[-1] * np.exp(drift + shock)
           prices.append(price)
       simulations.append(prices)
   ```

3. **Calculate Statistics:**
   ```python
   final_prices = [sim[-1] for sim in simulations]
   
   expected_price = np.mean(final_prices)
   median_price = np.median(final_prices)
   std_dev = np.std(final_prices)
   
   # Confidence intervals
   lower_bound_95 = np.percentile(final_prices, 2.5)
   upper_bound_95 = np.percentile(final_prices, 97.5)
   
   # Value at Risk
   var_5 = np.percentile(final_prices, 5)
   var_1 = np.percentile(final_prices, 1)
   ```

#### 3.3 Visualization

**Main Chart: Price Path Simulations**
- Plot 100 random paths (light gray, low opacity)
- Overlay mean path (orange, bold)
- Show confidence bands (shaded regions)
- X-axis: Days
- Y-axis: Price
- Interactive hover: day, price for each path

**Distribution Histogram**
- Final day prices distribution
- Color gradient by probability density
- Vertical lines for:
  - Current price (dashed gray)
  - Expected price (solid orange)
  - Confidence bounds (dashed orange)
- X-axis: Price
- Y-axis: Frequency

**Probability Table**
```
┌───────────────────────────────────────────────────┐
│         MONTE CARLO SIMULATION RESULTS            │
├───────────────────────────────────────────────────┤
│ Current Price:                    $178.25         │
│ Simulation Period:                30 days         │
│ Number of Simulations:            5,000           │
│ Confidence Level:                 95%             │
├───────────────────────────────────────────────────┤
│ Expected Price (Mean):            $185.30         │
│ Median Price:                     $184.10         │
│ Standard Deviation:               $12.45          │
├───────────────────────────────────────────────────┤
│ 95% Confidence Interval:                          │
│   Lower Bound (2.5%):            $162.50         │
│   Upper Bound (97.5%):           $210.75         │
├───────────────────────────────────────────────────┤
│ Probability Price Increases:      62.4%          │
│ Probability Price Decreases:      37.6%          │
├───────────────────────────────────────────────────┤
│ Value at Risk (VaR):                              │
│   95% VaR:                       -$8.75          │
│   99% VaR:                       -$15.20         │
├───────────────────────────────────────────────────┤
│ Expected Return:                  +3.96%          │
│ Risk/Reward Ratio:                1.85            │
└───────────────────────────────────────────────────┘
```

**Scenario Analysis**
```
┌───────────────┬───────────────┬─────────────┬──────────────┐
│ Scenario      │ Probability   │ Price Range │ Return       │
├───────────────┼───────────────┼─────────────┼──────────────┤
│ Best Case     │ 5%           │ >$210.00    │ >+17.8%      │
│ Bull Case     │ 20%          │ $195-$210   │ +9.4% - +17.8% │
│ Base Case     │ 50%          │ $175-$195   │ -1.8% - +9.4%│
│ Bear Case     │ 20%          │ $160-$175   │ -10.2% - -1.8%│
│ Worst Case    │ 5%           │ <$160.00    │ <-10.2%      │
└───────────────┴───────────────┴─────────────┴──────────────┘
```

#### 3.4 Risk Warnings

Display prominently:
```
⚠️ DISCLAIMER
Monte Carlo simulations are statistical models based on historical data.
They do NOT predict future prices with certainty.

• Results assume historical patterns continue
• Black swan events are not modeled
• Market conditions can change rapidly
• Use for educational purposes only
• This is NOT financial advice
```

---

## 🎨 UI/UX SPECIFICATIONS

### Color System

**Primary Palette:**
```css
--primary-orange: #FF6B00;
--primary-orange-light: #FF8C00;
--primary-orange-dark: #CC5500;

--bg-dark: #0A0E17;
--bg-medium: #1A1F2E;
--bg-light: #252D3F;

--accent-blue: #00D9FF;
--accent-cyan: #00FFCC;

--success-green: #00FF88;
--warning-yellow: #FFB800;
--danger-red: #FF4466;

--text-primary: #FFFFFF;
--text-secondary: #B0B0B0;
--text-muted: #707070;

--border-default: #2A3544;
--border-hover: #FF6B00;
```

**State Colors:**
```css
--positive-change: #00FF88;
--negative-change: #FF4466;
--neutral-change: #888888;
```

### Typography

**Font Stack:**
```css
--font-primary: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
--font-mono: 'JetBrains Mono', 'Courier New', monospace;
```

**Font Sizes:**
```css
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
--text-4xl: 2.25rem;   /* 36px */
```

### Spacing System

```css
--space-1: 0.25rem;    /* 4px */
--space-2: 0.5rem;     /* 8px */
--space-3: 0.75rem;    /* 12px */
--space-4: 1rem;       /* 16px */
--space-5: 1.25rem;    /* 20px */
--space-6: 1.5rem;     /* 24px */
--space-8: 2rem;       /* 32px */
--space-10: 2.5rem;    /* 40px */
--space-12: 3rem;      /* 48px */
```

### Component Specifications

**Card Component:**
```css
.card {
    background: linear-gradient(135deg, #1e2433 0%, #252d3f 100%);
    border: 1px solid var(--border-default);
    border-radius: 12px;
    padding: var(--space-6);
    box-shadow: 0 4px 16px rgba(0,0,0,0.3);
    transition: all 0.3s ease;
}

.card:hover {
    border-color: var(--border-hover);
    box-shadow: 0 8px 24px rgba(255, 107, 0, 0.2);
    transform: translateY(-2px);
}
```

**Button Component:**
```css
.btn-primary {
    background: linear-gradient(90deg, #ff6b00 0%, #ff8c00 100%);
    color: white;
    padding: var(--space-3) var(--space-6);
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.btn-primary:hover {
    box-shadow: 0 0 20px rgba(255, 107, 0, 0.5);
    transform: scale(1.05);
}
```

**Table Component:**
```css
.table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
}

.table thead {
    background: var(--bg-light);
    color: var(--primary-orange);
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.table tbody tr {
    border-bottom: 1px solid var(--border-default);
    transition: all 0.2s ease;
}

.table tbody tr:hover {
    background: rgba(255, 107, 0, 0.05);
    cursor: pointer;
}
```

### Animation Guidelines

**Transitions:**
- Default duration: 0.3s
- Easing: ease-in-out
- Use for: hover, focus, state changes

**Loading States:**
- Skeleton screens for data loading
- Pulse animation for loading indicators
- Progress bars for long operations

**Micro-interactions:**
- Button press: scale(0.95)
- Card hover: translateY(-2px)
- Icon hover: rotate or scale

---

## 🔧 TECHNICAL IMPLEMENTATION

### Data Fetching Strategy

**yfinance Integration:**
```python
import yfinance as yf

# Single stock
def fetch_stock_data(symbol):
    ticker = yf.Ticker(symbol)
    info = ticker.info
    history = ticker.history(period="1y")
    return {
        "info": info,
        "history": history
    }

# Multiple stocks (optimized)
def fetch_multiple_stocks(symbols):
    data = yf.download(
        tickers=symbols,
        period="1d",
        interval="1d",
        group_by='ticker',
        threads=True
    )
    return data
```

**Caching Strategy:**
```python
import streamlit as st
from functools import lru_cache
from datetime import datetime, timedelta

@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_stock_data(symbol):
    return fetch_stock_data(symbol)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_historical_data(symbol, period):
    ticker = yf.Ticker(symbol)
    return ticker.history(period=period)
```

### State Management

**Session State Schema:**
```python
# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = load_portfolio()

if 'pinned_stocks' not in st.session_state:
    st.session_state.pinned_stocks = load_pinned_stocks()

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'dashboard'

if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = None
```

### Data Persistence

**JSON Storage:**
```python
import json
from pathlib import Path

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

def save_portfolio(portfolio):
    with open(DATA_DIR / "portfolio.json", "w") as f:
        json.dump(portfolio, f, indent=2, default=str)

def load_portfolio():
    try:
        with open(DATA_DIR / "portfolio.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"positions": [], "metadata": {}}
```

### Error Handling

**Network Errors:**
```python
def safe_fetch_stock(symbol):
    try:
        data = yf.Ticker(symbol).info
        return {"success": True, "data": data}
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Unable to fetch stock data. Please try again."
        }
```

**User Input Validation:**
```python
def validate_ticker(symbol):
    if not symbol or len(symbol) > 10:
        return False, "Invalid ticker length"
    
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info
        if 'regularMarketPrice' not in info:
            return False, "Ticker not found"
        return True, "Valid ticker"
    except:
        return False, "Ticker not found"
```

---

## 📊 PERFORMANCE REQUIREMENTS

### Response Times
- Initial page load: < 3 seconds
- Dashboard refresh: < 2 seconds
- Portfolio calculations: < 1 second
- Monte Carlo simulation (5000 runs): < 5 seconds
- Stock search autocomplete: < 500ms

### Data Limits
- Portfolio positions: Max 100
- Pinned stocks: Max 5
- Historical data: Up to 10 years
- Monte Carlo simulations: Max 10,000 runs

### Browser Support
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 🔒 SECURITY CONSIDERATIONS

### Data Privacy
- All data stored locally
- No user authentication required (MVP)
- No data transmission to external servers (except yfinance API)

### Input Sanitization
- Validate all user inputs
- Prevent SQL injection (not applicable for JSON)
- Sanitize file names for exports

### API Rate Limiting
- Respect yfinance rate limits
- Implement exponential backoff
- Cache frequently requested data

---

## 🧪 TESTING STRATEGY

### Unit Tests
- Data fetching functions
- Calculation utilities
- Validation logic

### Integration Tests
- Complete user workflows
- Data persistence
- State management

### User Acceptance Tests
- Navigation flows
- Data accuracy
- Visual appearance
- Error handling

---

**Document Version**: 1.0
**Last Updated**: March 29, 2026
**Status**: Ready for Implementation
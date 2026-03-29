BBG_BLACK = "#000000"
BBG_DARK_GRAY = "#0D0D0D"
BBG_PANEL = "#1A1A1A"
BBG_PANEL_BORDER = "#333333"
BBG_TEXT = "#FFFFFF"
BBG_TEXT_DIM = "#999999"
BBG_GREEN = "#00FF00"
BBG_RED = "#FF0000"
BBG_YELLOW = "#FFFF00"
BBG_BLUE = "#00AAFF"
BBG_ORANGE = "#FF9900"

BACKGROUND_DARK = BBG_BLACK
BACKGROUND_CARD = BBG_PANEL
TEXT_PRIMARY = BBG_TEXT
TEXT_SECONDARY = BBG_TEXT_DIM
ACCENT_BLUE = BBG_BLUE
SUCCESS_GREEN = BBG_GREEN
DANGER_RED = BBG_RED
WARNING_YELLOW = BBG_YELLOW
PRIMARY_ORANGE = BBG_ORANGE

STREAMLIT_THEME = {
    "primaryColor": BBG_ORANGE,
    "backgroundColor": BBG_BLACK,
    "secondaryBackgroundColor": BBG_PANEL,
    "textColor": BBG_TEXT,
    "font": "monospace",
}

CUSTOM_CSS = f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600;700&display=swap');
    
    .stApp {{
        background-color: {BBG_BLACK};
        font-family: 'JetBrains Mono', monospace;
    }}
    
    /* Main content area */
    .main .block-container {{
        background-color: {BBG_BLACK};
        padding-top: 1rem;
    }}
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'JetBrains Mono', monospace;
        color: {BBG_TEXT};
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Sidebar */
    [data-testid="stSidebar"] {{
        background-color: {BBG_DARK_GRAY};
        border-right: 1px solid {BBG_PANEL_BORDER};
    }}
    
    /* Tabs - Bloomberg style */
    .stTabs [data-baseweb="tab-list"] {{
        background-color: {BBG_DARK_GRAY};
        border-bottom: 2px solid {BBG_ORANGE};
        gap: 0px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {BBG_DARK_GRAY};
        color: {BBG_TEXT_DIM};
        font-family: 'JetBrains Mono', monospace;
        font-weight: 500;
        text-transform: uppercase;
        font-size: 12px;
        padding: 10px 20px;
        border: none;
    }}
    
    .stTabs [data-baseweb="tab"]:hover {{
        background-color: {BBG_PANEL};
        color: {BBG_TEXT};
    }}
    
    .stTabs [aria-selected="true"] {{
        background-color: {BBG_PANEL} !important;
        color: {BBG_ORANGE} !important;
        border-top: 2px solid {BBG_ORANGE};
        border-left: 1px solid {BBG_PANEL_BORDER};
        border-right: 1px solid {BBG_PANEL_BORDER};
    }}
    
    /* Dataframe - Bloomberg style */
    .stDataFrame {{
        background-color: {BBG_PANEL};
        border: 1px solid {BBG_PANEL_BORDER};
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
    }}
    
    .stDataFrame thead {{
        background-color: {BBG_DARK_GRAY};
        color: {BBG_ORANGE};
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 600;
    }}
    
    .stDataFrame tbody tr {{
        border-bottom: 1px solid {BBG_PANEL_BORDER};
    }}
    
    .stDataFrame tbody tr:hover {{
        background-color: #252525;
    }}
    
    /* Metrics - Bloomberg style */
    [data-testid="stMetric"] {{
        background-color: {BBG_PANEL};
        border: 1px solid {BBG_PANEL_BORDER};
        padding: 15px;
        border-radius: 0;
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {BBG_TEXT_DIM};
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        font-size: 10px;
        letter-spacing: 1px;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {BBG_TEXT};
        font-family: 'JetBrains Mono', monospace;
        font-size: 24px;
        font-weight: 700;
    }}
    
    /* Expander */
    [data-testid="stExpander"] {{
        background-color: {BBG_PANEL};
        border: 1px solid {BBG_PANEL_BORDER};
        border-radius: 0;
    }}
    
    /* Buttons */
    .stButton > button {{
        background-color: {BBG_DARK_GRAY};
        color: {BBG_TEXT};
        border: 1px solid {BBG_PANEL_BORDER};
        border-radius: 0;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 500;
    }}
    
    .stButton > button:hover {{
        background-color: {BBG_PANEL};
        border-color: {BBG_ORANGE};
        color: {BBG_ORANGE};
    }}
    
    /* Primary button */
    .stButton > button[kind="primary"] {{
        background-color: {BBG_ORANGE};
        color: {BBG_BLACK};
        border: none;
        font-weight: 700;
    }}
    
    .stButton > button[kind="primary"]:hover {{
        background-color: {BBG_YELLOW};
    }}
    
    /* Selectbox/Dropdown */
    .stSelectbox > div > div {{
        background-color: {BBG_DARK_GRAY};
        border: 1px solid {BBG_PANEL_BORDER};
        border-radius: 0;
    }}
    
    /* Text Input */
    .stTextInput > div > div {{
        background-color: {BBG_DARK_GRAY};
        border: 1px solid {BBG_PANEL_BORDER};
        border-radius: 0;
    }}
    
    .stTextInput input {{
        font-family: 'JetBrains Mono', monospace;
        color: {BBG_TEXT};
    }}
    
    /* Number Input */
    .stNumberInput > div > div {{
        background-color: {BBG_DARK_GRAY};
        border: 1px solid {BBG_PANEL_BORDER};
        border-radius: 0;
    }}
    
    /* Date Input */
    .stDateInput > div > div {{
        background-color: {BBG_DARK_GRAY};
        border: 1px solid {BBG_PANEL_BORDER};
        border-radius: 0;
    }}
    
    /* Forms */
    .stForm {{
        background-color: {BBG_PANEL};
        border: 1px solid {BBG_PANEL_BORDER};
        padding: 20px;
        border-radius: 0;
    }}
    
    /* Dividers */
    hr {{
        border-color: {BBG_PANEL_BORDER};
    }}
    
    /* Spinners */
    .stSpinner > div {{
        border-color: {BBG_ORANGE};
    }}
    
    /* Alerts/Info boxes */
    .stAlert {{
        border-radius: 0;
        border-left: 3px solid {BBG_ORANGE};
    }}
    
    /* Positive/Negative colors */
    .positive {{
        color: {BBG_GREEN} !important;
    }}
    
    .negative {{
        color: {BBG_RED} !important;
    }}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {BBG_BLACK};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {BBG_PANEL_BORDER};
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {BBG_ORANGE};
    }}
    
    /* Bloomberg Panel styling */
    .bbg-panel {{
        background-color: {BBG_PANEL};
        border: 1px solid {BBG_PANEL_BORDER};
        padding: 10px;
        margin: 5px 0;
    }}
    
    .bbg-header {{
        background-color: {BBG_DARK_GRAY};
        color: {BBG_ORANGE};
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 11px;
        padding: 5px 10px;
        border-bottom: 1px solid {BBG_PANEL_BORDER};
        letter-spacing: 1px;
    }}
    
    .bbg-data {{
        font-family: 'JetBrains Mono', monospace;
        color: {BBG_TEXT};
        font-size: 12px;
    }}
    
    .bbg-value {{
        color: {BBG_TEXT};
        font-weight: 500;
    }}
    
    .bbg-change-up {{
        color: {BBG_GREEN};
    }}
    
    .bbg-change-down {{
        color: {BBG_RED};
    }}
    
    /* Radio buttons - Bloomberg sidebar style */
    .stRadio {{
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .stRadio > div {{
        background-color: transparent;
        padding: 0;
    }}
    
    .stRadio label {{
        font-family: 'JetBrains Mono', monospace !important;
        color: #999999;
        font-size: 12px;
        padding: 10px 15px;
        border-radius: 0;
        transition: all 0.2s;
        margin: 2px 0;
        border: 1px solid transparent;
    }}
    
    .stRadio label:hover {{
        background-color: #1A1A1A;
        color: #FFFFFF;
    }}
    
    .stRadio [data-baseweb="radio"]:checked + div > label,
    .stRadio label:has(input:checked) {{
        background-color: #1A1A1A !important;
        color: #FF9900 !important;
        border-left: 3px solid #FF9900;
    }}
    
    .stRadio [data-baseweb="radio"] {{
        background-color: transparent;
    }}
    
    .stRadio span {{
        color: #999999;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    .stRadio p {{
        font-family: 'JetBrains Mono', monospace;
        color: #999999;
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }}
    
    /* Sidebar elements styling */
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4 {{
        color: #FFFFFF;
        font-family: 'JetBrains Mono', monospace;
    }}
    
    [data-testid="stSidebar"] hr {{
        border-color: #333333;
    }}
    
    /* Sidebar selectbox styling */
    [data-testid="stSidebar"] .stSelectbox > div > div {{
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 0;
    }}
    
    [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {{
        background-color: #1A1A1A;
    }}
    
    /* Sidebar input styling */
    [data-testid="stSidebar"] .stTextInput > div > div,
    [data-testid="stSidebar"] .stNumberInput > div > div {{
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 0;
    }}
    
    [data-testid="stSidebar"] input {{
        font-family: 'JetBrains Mono', monospace;
        color: #FFFFFF;
    }}
    
    /* Sidebar expander */
    [data-testid="stSidebar"] [data-testid="stExpander"] {{
        background-color: #1A1A1A;
        border: 1px solid #333333;
        border-radius: 0;
    }}
    
    /* Sidebar button styling */
    [data-testid="stSidebar"] .stButton > button {{
        width: 100%;
        background-color: #0D0D0D;
        color: #FFFFFF;
        border: 1px solid #333333;
        border-radius: 0;
        font-family: 'JetBrains Mono', monospace;
        text-transform: uppercase;
        font-size: 11px;
        font-weight: 500;
    }}
    
    [data-testid="stSidebar"] .stButton > button:hover {{
        background-color: #1A1A1A;
        border-color: #FF9900;
        color: #FF9900;
    }}
    
    /* Plotly charts */
    .js-plotly-plot .plotly {{
        background-color: #000000;
    }}
</style>
"""

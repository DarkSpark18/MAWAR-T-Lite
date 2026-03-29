import os

APP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP_TITLE = "MAWAR T Lite"
APP_ICON = "📊"
APP_VERSION = "0.1.0"
APP_LOGO = os.path.join(APP_DIR, "assets", "images", "logo.png")
APP_FAVICON = os.path.join(APP_DIR, "assets", "images", "favicon.ico")

CACHE_TTL = 60
AUTO_REFRESH_INTERVAL = 300
MAX_PINNED_STOCKS = 5

MAX_PORTFOLIO_SIZE = 100
DEFAULT_CURRENCY = "USD"

DEFAULT_SIMULATIONS = 5000
MAX_SIMULATIONS = 10000
DEFAULT_CONFIDENCE = 95

import os

from dotenv import load_dotenv

load_dotenv()

# ==========================================
# Discord
# ==========================================

DISCORD_WEBHOOK_URL = os.getenv(
    "DISCORD_WEBHOOK_URL"
)

# ==========================================
# Crypto mapping
# ==========================================

SYMBOL_MAPPING = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "hyperliquid": "HYPE",
    "akash-network": "AKT",
    "aethir": "ATH"
}

# ==========================================
# Watchlist (.env)
# ==========================================

WATCHLIST = {
    coin: SYMBOL_MAPPING.get(
        coin,
        coin.upper()
    )
    for coin in os.getenv(
        "WATCHLIST",
        ""
    ).split(",")
    if coin
}

# ==========================================
# Scheduling
# ==========================================

REPORT_HOUR = os.getenv(
    "REPORT_HOUR",
    "07"
)

REPORT_TIME = (
    f"{REPORT_HOUR}:30"
)

TIMEZONE = os.getenv(
    "TZ",
    "Europe/Paris"
)

ALERT_INTERVAL_MINUTES = 30

# ==========================================
# Market thresholds
# ==========================================

PUMP_THRESHOLD = 10
DUMP_THRESHOLD = -7

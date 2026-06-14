"""
=========================================================
Captain Cryptos - Main Scheduler
=========================================================

Responsabilités
----------------
✅ Rapport quotidien Discord
✅ Rapport au démarrage container
✅ Alertes marché toutes les 30 min
✅ Scheduler robuste
✅ Orchestration des modules

Architecture
-------------
config.py
    configuration globale

market.py
    données CoinGecko
    Fear & Greed
    format prix

report.py
    génération rapport

discord_notify.py
    webhook Discord

alerts.py
    alertes pump/dump

scoring.py
    score opportunité

data/state.json
    anti-spam alertes

Version :
    MVP v1.5
=========================================================
"""

import time
import schedule

from config import (
    DISCORD_WEBHOOK_URL,
    REPORT_TIME,
    ALERT_INTERVAL_MINUTES
)

from market import (
    get_market_data,
    format_price
)

from report import (
    build_report
)

from alerts import (
    check_alerts
)

from discord_notify import (
    send_discord_message
)


def send_report():

    print(
        "Génération du rapport..."
    )

    market_data = (
        get_market_data()
    )

    if not market_data:

        print(
            "Aucune donnée marché."
        )

        return

    report = (
        build_report(
            market_data
        )
    )

    print(report)

    send_discord_message(
        DISCORD_WEBHOOK_URL,
        report
    )

    check_alerts(
        market_data,
        DISCORD_WEBHOOK_URL,
        format_price
    )


def run_alerts():

    market_data = (
        get_market_data()
    )

    if not market_data:

        print(
            "Pas de données "
            "pour alertes."
        )

        return

    check_alerts(
        market_data,
        DISCORD_WEBHOOK_URL,
        format_price
    )


print(
    "Crypto assistant démarré "
    f"(rapport {REPORT_TIME}, "
    f"alertes "
    f"{ALERT_INTERVAL_MINUTES} min)"
)

# Rapport au démarrage
print(
    "Envoi rapport "
    "de démarrage..."
)

send_report()

# Rapport quotidien
schedule.every().day.at(
    REPORT_TIME
).do(
    send_report
)

# Alertes marché
schedule.every(
    ALERT_INTERVAL_MINUTES
).minutes.do(
    run_alerts
)

while True:

    try:

        schedule.run_pending()

    except Exception as e:

        print(
            f"Scheduler error: {e}"
        )

    time.sleep(60)

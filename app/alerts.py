import json
import os
import requests

from config import (
    PUMP_THRESHOLD,
    DUMP_THRESHOLD
)

STATE_FILE = "/app/data/state.json"


def load_state():

    if not os.path.exists(
        STATE_FILE
    ):
        return {}

    try:

        with open(
            STATE_FILE,
            "r"
        ) as f:

            return json.load(f)

    except Exception:

        return {}


def save_state(state):

    with open(
        STATE_FILE,
        "w"
    ) as f:

        json.dump(
            state,
            f
        )


def check_alerts(
    market_data,
    webhook_url,
    format_price
):

    state = load_state()

    for coin in market_data:

        symbol = (
            coin["symbol"]
            .upper()
        )

        price_usd = (
            coin["current_price"]
        )

        price_eur = coin.get(
            "eur_price",
            0
        )

        change_24h = coin.get(
            "price_change_percentage_24h_in_currency",
            0
        )

        last_alert = state.get(
            symbol
        )

        alert_type = None
        message = None

        # DUMP

        if ( change_24h <= DUMP_THRESHOLD ):


            alert_type = "dump"

            message = (
                "━━━━━━━━━━━━━━\n"
                f"🚨 **{symbol}**\n\n"
                f"Forte baisse détectée\n\n"
                f"💰 Prix : "
                f"{format_price(price_eur, 'EUR')} / "
                f"{format_price(price_usd, 'USD')}\n"
                f"📉 24h : "
                f"{change_24h:+.2f}%\n\n"
                f"➡ Possible zone "
                f"de DCA progressif.\n"
                "━━━━━━━━━━━━━━"
            )

        # PUMP
        elif ( change_24h >= PUMP_THRESHOLD ):

            alert_type = "pump"

            message = (
                "━━━━━━━━━━━━━━\n"
                f"🚀 **{symbol}**\n\n"
                f"Forte hausse détectée\n\n"
                f"💰 Prix : "
                f"{format_price(price_eur, 'EUR')} / "
                f"{format_price(price_usd, 'USD')}\n"
                f"📈 24h : "
                f"{change_24h:+.2f}%\n\n"
                f"➡ Prudence FOMO.\n"
                "━━━━━━━━━━━━━━"
            )

        # éviter doublons
        if (
            alert_type
            and last_alert
            == alert_type
        ):
            continue

        # envoyer alerte
        if alert_type:

            try:

                requests.post(
                    webhook_url,
                    json={
                        "content":
                        message
                    },
                    timeout=10
                )

                print(
                    f"Alerte "
                    f"{alert_type} "
                    f"envoyée "
                    f"pour "
                    f"{symbol}"
                )

                # mémoriser état
                state[
                    symbol
                ] = (
                    alert_type
                )

            except Exception as e:

                print(
                    f"Alert Discord error: {e}"
                )

        # reset état si retour normal
        else:

            if (
                symbol
                in state
            ):

                print(
                    f"Reset alerte "
                    f"{symbol}"
                )

                state.pop(
                    symbol,
                    None
                )

    save_state(state)

from config import (
    WATCHLIST
)

from market import (
    get_fear_greed,
    format_price
)

from scoring import (
    calculate_score,
    score_message
)


def build_report(
    market_data
):

    fear_value, fear_label = (
        get_fear_greed()
    )

    report = (
        "📊 **Rapport Crypto**\n\n"
    )

    report += (
        f"🌍 **Marché**\n"
        f"Fear & Greed : "
        f"**{fear_value}** "
        f"({fear_label})\n\n"
    )

    separator = (
        "━━━━━━━━━━━━━━\n"
    )

    for coin in market_data:

        symbol = (
            WATCHLIST.get(
                coin["id"],
                coin[
                    "symbol"
                ].upper()
            )
        )

        usd_price = (
            coin[
                "current_price"
            ]
        )

        eur_price = coin.get(
            "eur_price",
            0
        )

        change_24h = (
            coin.get(
                "price_change_percentage_24h_in_currency",
                0
            )
        )

        change_7d = (
            coin.get(
                "price_change_percentage_7d_in_currency",
                0
            )
        )

        score = calculate_score(
            coin,
            fear_value
        )

        score_text = (
            score_message(
                score
            )
        )

        report += (
            separator +
            f"**{symbol}**\n"
            f"💰 **Prix** : "
            f"{format_price(eur_price, 'EUR')} "
            f"/ "
            f"{format_price(usd_price, 'USD')}\n"
            f"📈 **24h** : "
            f"{change_24h:+.2f}%\n"
            f"📊 **7j** : "
            f"{change_7d:+.2f}%\n"
            f"🎯 **Score** : "
            f"**{score}/100**\n"
            f"➡ {score_text}\n\n"
        )

    return report

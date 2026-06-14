
from config import (
    WATCHLIST
)

from market import (
    format_price
)

from scoring import (
    calculate_score,
    score_message
)


def get_market_context(
    fear_value
):

    fear_value = int(
        fear_value
    )

    if fear_value <= 25:

        return (
            "🟢 **Contexte**\n"
            "Marché en peur extrême.\n"
            "DCA progressif "
            "renforcé possible.\n"
        )

    elif fear_value <= 45:

        return (
            "🟡 **Contexte**\n"
            "Marché prudent.\n"
            "DCA normal "
            "possible.\n"
        )

    elif fear_value <= 65:

        return (
            "🟠 **Contexte**\n"
            "Marché neutre.\n"
            "Rester sélectif.\n"
        )

    elif fear_value <= 80:

        return (
            "🔴 **Contexte**\n"
            "Marché euphorique.\n"
            "Prudence FOMO.\n"
        )

    return (
        "🚨 **Contexte**\n"
        "Euphorie extrême.\n"
        "Réduire le DCA.\n"
    )


def format_market_volume(
    volume
):

    if volume >= 1_000_000_000:

        return (
            f"{volume / 1_000_000_000:.1f}B $"
        )

    return (
        f"{volume:,.0f} $"
    )


def get_macro_comment(
    macro_data
):

    btc_dom = (
        macro_data[
            "btc_dominance"
        ]
    )

    stable_dom = (
        macro_data[
            "stable_dominance"
        ]
    )

    volume = (
        macro_data[
            "global_volume_usd"
        ]
    )

    # BTC dominance
    if btc_dom >= 60:

        btc_comment = (
            "→ BTC domine "
            "fortement le marché"
        )

    elif btc_dom >= 55:

        btc_comment = (
            "→ BTC reste dominant"
        )

    else:

        btc_comment = (
            "→ Rotation altcoins "
            "possible"
        )

    # Stable dominance
    if stable_dom >= 10:

        stable_comment = (
            "→ Beaucoup de "
            "liquidités en attente"
        )

    else:

        stable_comment = (
            "→ Argent déjà "
            "largement investi"
        )

    # Volume
    if volume >= 100_000_000_000:

        volume_comment = (
            "→ Marché très actif"
        )

    elif volume >= 50_000_000_000:

        volume_comment = (
            "→ Activité correcte"
        )

    else:

        volume_comment = (
            "→ Marché plutôt calme"
        )

    return (
        f"₿ **BTC dominance** : "
        f"{btc_dom:.2f}%\n"
        f"{btc_comment}\n\n"

        f"💵 **Stable dominance** : "
        f"{stable_dom:.2f}%\n"
        f"{stable_comment}\n\n"

        f"📊 **Volume global** : "
        f"{format_market_volume(volume)}\n"
        f"{volume_comment}\n"
    )


def build_report(
    market_data,
    macro_data
):

    fear_value = (
        macro_data[
            "fear_value"
        ]
    )

    fear_label = (
        macro_data[
            "fear_label"
        ]
    )

    report = (
        "📊 **Rapport Crypto**\n\n"
    )

    market_context = (
        get_market_context(
            fear_value
        )
    )

    macro_comment = (
        get_macro_comment(
            macro_data
        )
    )

    report += (
        f"🌍 **Marché**\n"
        f"Fear & Greed : "
        f"**{fear_value}** "
        f"({fear_label})\n\n"
        f"{market_context}\n"
        f"📈 **Macro**\n\n"
        f"{macro_comment}\n"
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

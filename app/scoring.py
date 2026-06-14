def calculate_score(
    coin,
    fear_value
):

    score = 50

    change_24h = coin.get(
        "price_change_percentage_24h_in_currency",
        0
    )

    change_7d = coin.get(
        "price_change_percentage_7d_in_currency",
        0
    )

    ath_change = abs(
        coin.get(
            "ath_change_percentage",
            0
        )
    )

    symbol = (
        coin["symbol"]
        .upper()
    )

    # Fear & Greed
    fear_value = int(
        fear_value
    )

    if fear_value <= 20:
        score += 20

    elif fear_value <= 35:
        score += 10

    elif fear_value >= 75:
        score -= 15

    elif fear_value >= 60:
        score -= 8

    # 24h momentum
    if change_24h <= -10:
        score += 18

    elif change_24h <= -5:
        score += 10

    elif change_24h >= 10:
        score -= 20

    elif change_24h >= 5:
        score -= 10

    # 7 days trend
    if change_7d <= -15:
        score -= 10

    elif change_7d <= -7:
        score -= 5

    # Distance ATH
    if ath_change >= 80:
        score += 5

    elif ath_change <= 15:
        score -= 5

    # Stability bonus
    if symbol == "BTC":
        score += 8

    elif symbol == "ETH":
        score += 5

    score = max(
        0,
        min(
            score,
            100
        )
    )

    return score


def score_message(
    score
):

    if score >= 80:
        return (
            "🟢 DCA progressif "
            "intéressant"
        )

    if score >= 65:
        return (
            "🟡 Contexte "
            "plutôt favorable"
        )

    if score >= 45:
        return (
            "🟠 Attendre "
            "confirmation"
        )

    return (
        "🔴 Prudence "
        "FOMO / risque"
    )

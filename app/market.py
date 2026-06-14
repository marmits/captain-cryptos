import requests

from config import (
    WATCHLIST
)


def get_fear_greed():

    try:

        response = requests.get(
            "https://api.alternative.me/fng/?limit=1",
            timeout=10
        )

        data = response.json()[
            "data"
        ][0]

        return (
            data["value"],
            data[
                "value_classification"
            ]
        )

    except Exception as e:

        print(
            f"Fear & Greed error: {e}"
        )

        return "?", "Unknown"


def get_market_data():

    ids = ",".join(
        WATCHLIST.keys()
    )

    url = (
        "https://api.coingecko.com/api/v3/coins/markets"
    )

    params = {
        "vs_currency": "usd",
        "ids": ids,
        "price_change_percentage":
        "24h,7d",
        "sparkline": "false",
        "precision": "full"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if (
            response.status_code
            == 429
        ):

            print(
                "CoinGecko rate limit"
            )

            return []

        response.raise_for_status()

        market_data = (
            response.json()
        )

        eur_prices = (
            get_eur_prices()
        )

        for coin in market_data:

            coin_id = coin["id"]

            if (
                coin_id
                in eur_prices
            ):

                coin[
                    "eur_price"
                ] = eur_prices[
                    coin_id
                ]["eur"]

        return market_data

    except Exception as e:

        print(
            f"Market data error: {e}"
        )

        return []


def get_eur_prices():

    ids = ",".join(
        WATCHLIST.keys()
    )

    url = (
        "https://api.coingecko.com/api/v3/simple/price"
    )

    params = {
        "ids": ids,
        "vs_currencies":
        "eur"
    }

    try:

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if (
            response.status_code
            == 429
        ):

            print(
                "EUR API rate limit"
            )

            return {}

        response.raise_for_status()

        return response.json()

    except Exception as e:

        print(
            f"EUR prices error: {e}"
        )

        return {}


def format_price(
    price,
    currency
):

    symbol = (
        "€"
        if currency
        == "EUR"
        else "$"
    )

    if price >= 1000:

        formatted = (
            f"{price:,.0f}"
        )

    elif price >= 1:

        formatted = (
            f"{price:,.2f}"
        )

    elif price >= 0.01:

        formatted = (
            f"{price:.4f}"
        )

    else:

        formatted = (
            f"{price:.6f}"
        )

    formatted = (
        formatted
        .replace(",", " ")
    )

    return (
        f"{formatted} "
        f"{symbol}"
    )

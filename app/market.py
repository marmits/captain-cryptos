import requests

from config import (
    WATCHLIST
)


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


def get_macro_data():

    try:

        # Fear & Greed
        fear_response = requests.get(
            "https://api.alternative.me/fng/?limit=1",
            timeout=10
        )

        fear_data = (
            fear_response.json()
            ["data"][0]
        )

        fear_value = int(
            fear_data["value"]
        )

        fear_label = (
            fear_data[
                "value_classification"
            ]
        )

        # CoinGecko Global
        cg_response = requests.get(
            "https://api.coingecko.com/api/v3/global",
            timeout=10
        )

        if (
            cg_response.status_code
            == 429
        ):

            print(
                "CoinGecko macro "
                "rate limit"
            )

            return {}

        cg_response.raise_for_status()

        data = (
            cg_response.json()
            ["data"]
        )

        # BTC dominance
        btc_dominance = (
            data[
                "market_cap_percentage"
            ].get(
                "btc",
                0
            )
        )

        # Global volume
        global_volume = (
            data[
                "total_volume"
            ].get(
                "usd",
                0
            )
        )

        # Stablecoin dominance
        stablecoins = [
            "usdt",
            "usdc",
            "dai",
            "fdusd",
            "usde"
        ]

        stable_dominance = 0

        for stable in stablecoins:

            stable_dominance += (
                data[
                    "market_cap_percentage"
                ].get(
                    stable,
                    0
                )
            )

        # DXY
        # DXY (désactivé V1)
        #dxy = get_dxy()
        dxy = None
        

        return {

            "fear_value":
            fear_value,

            "fear_label":
            fear_label,

            "btc_dominance":
            round(
                btc_dominance,
                2
            ),

            "global_volume_usd":
            round(
                global_volume,
                0
            ),

            "stable_dominance":
            round(
                stable_dominance,
                2
            ),

            "dxy":
            dxy
        }

    except Exception as e:

        print(
            f"Macro error: {e}"
        )

        return {}


def get_dxy():

    try:

        response = requests.get(
            "https://stooq.com/q/l/?s=dx.f&f=sd2t2ohlcv&h&e=json",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return float(
            data[
                "symbols"
            ][0][
                "close"
            ]
        )

    except Exception as e:

        print(
            f"DXY error: {e}"
        )

        return None


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

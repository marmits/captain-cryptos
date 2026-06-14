import requests
import time

from config import (
    WATCHLIST,
    COINGECKO_API_KEY
)

HEADERS = {
    "User-Agent":
    "CaptainCryptos/1.0"
}


def safe_get(
    url,
    params=None
):

    for attempt in range(2):

        try:

            headers = HEADERS.copy()

            if (
                COINGECKO_API_KEY
                and "coingecko.com"
                in url
            ):

                headers[
                    "x-cg-demo-api-key"
                ] = (
                    COINGECKO_API_KEY
                )

            response = requests.get(
                url,
                params=params,
                headers=headers,
                timeout=10
            )

            if (
                response.status_code
                == 429
            ):

                print(
                    "Rate limit API "
                    f"(tentative {attempt+1})"
                )

                time.sleep(2)

                continue

            response.raise_for_status()

            return response

        except Exception as e:

            print(
                f"Request error: {e}"
            )

            time.sleep(2)

    return None


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

    response = safe_get(
        url,
        params
    )

    if not response:

        return []

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

    response = safe_get(
        url,
        params
    )

    if not response:

        print(
            "EUR API rate limit"
        )

        return {}

    return response.json()


def get_macro_data():

    try:

        # Fear & Greed
        fear_response = safe_get(
            "https://api.alternative.me/fng/?limit=1"
        )

        if not fear_response:

            return {}

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

        # CoinGecko global
        cg_response = safe_get(
            "https://api.coingecko.com/api/v3/global"
        )

        if not cg_response:

            print(
                "CoinGecko macro "
                "rate limit"
            )

            return {}

        data = (
            cg_response.json()
            ["data"]
        )

        btc_dominance = (
            data[
                "market_cap_percentage"
            ].get(
                "btc",
                0
            )
        )

        global_volume = (
            data[
                "total_volume"
            ].get(
                "usd",
                0
            )
        )

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

        response = safe_get(
            "https://stooq.com/q/l/?s=dx.f&f=sd2t2ohlcv&h&e=json"
        )

        if not response:

            return None

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


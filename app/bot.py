import discord
from discord.ext import commands

from config import (
    DISCORD_BOT_TOKEN
)

from market import (
    get_market_data,
    get_macro_data
)

from report import (
    build_report
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():

    print(
        f"✅ Bot connecté : "
        f"{bot.user}"
    )


@bot.command()
async def report(ctx):

    await ctx.send(
        "📊 Génération du rapport..."
    )

    try:

        market_data = (
            get_market_data()
        )

        if not market_data:

            await ctx.send(
                "❌ Impossible de "
                "récupérer le marché."
            )

            return

        macro_data = (
            get_macro_data()
        )

        # fallback si CoinGecko rate limit
        if not macro_data:

            print(
                "Macro indisponible, "
                "fallback utilisé."
            )

            macro_data = {
                "fear_value": 50,
                "fear_label": "Unavailable",
                "btc_dominance": 0,
                "global_volume_usd": 0,
                "stable_dominance": 0,
                "dxy": None
            }

        report = (
            build_report(
                market_data,
                macro_data
            )
        )

        await ctx.send(report)

    except Exception as e:

        print(
            f"Bot report error: {e}"
        )

        await ctx.send(
            "❌ Erreur génération "
            "rapport."
        )


bot.run(
    DISCORD_BOT_TOKEN
)
import interactions
import pandas as pd

import queries

TOKEN = 'MTAyMDYzNDY4MDMzNDIzMzYyMQ.G5Zywf.SZvkjN3sEII_ze3Y3EsGUTPUJJhAhgPlFhpeKI'
GUILD_ID = 1020432806461063169
bot = interactions.Client(token=TOKEN)


# @bot.command(
#    name="Dune Query Content",
#    description="Get Dune Query Content",
#    scope=GUILD_ID,
#    options=[
#       interactions.Option(
#            name="text",
#            description="Dune Query ID",
#            type=interactions.OptionType.STRING,
#            required=True,
#        ),
#    ],
# )
@bot.command(
    name="get_dune_query_content",
    description="Get the Dune Query Content as Table/Plot",
    scope=GUILD_ID,
    options=[
        interactions.Option(
            name="query_id",
            description="Dune Query ID",
            type=interactions.OptionType.STRING,
            required=True,
        ),
    ],
)
async def my_first_command(ctx: interactions.CommandContext, query_id: str):
    data: pd.DataFrame = queries.get_query_content(query_id)
    await ctx.send(data.to_string())


bot.start()

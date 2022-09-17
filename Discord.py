import interactions
import pandas as pd
import os
import queries

TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILDID'))

print(TOKEN, GUILD_ID)

bot = interactions.Client(token=TOKEN)


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

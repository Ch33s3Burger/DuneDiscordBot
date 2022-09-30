import os

import discord

from Cache import DuneQueryCache
from Models import Command

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

if DISCORD_BOT_TOKEN is None:
    raise EnvironmentError('Set Environment variable: DISCORD_BOT_TOKEN')
if GUILD_ID is None:
    raise EnvironmentError('Set Environment variable: GUILD_ID')

cache = DuneQueryCache()


class DiscordController(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user or not message.content.startswith('!'):
            return
        channel = client.get_channel(message.channel.id)
        command = Command(command=message.content, cache=cache)
        error_message = command.validate_command()
        if error_message is not None:
            await channel.send(f'Error Message: {error_message}')
            return
        await command.execute_command(channel)


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    client = DiscordController(intents=intents)
    client.run(DISCORD_BOT_TOKEN)

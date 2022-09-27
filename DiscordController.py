import asyncio
import functools
import os
import typing

import discord

import DuneApiConnector
import OutputFileCreator
from Models import Command

COMMAND_OPTIONS = ['dune', 'help']
OUTPUT_OPTION_TYPES = ['bar', 'line', 'scatter', 'table', 'single_value']
HELP_TEXT = 'Commands: !dune QUERY_ID + (RESULT_TYPE)\n\t' \
            'QUERY_ID: Dune Query ID\n\t' \
            'RESUlT_TYPE: Optional parameter to define result type. Options:\n\t\t' \
            'line: Line Graph\n\t\t' \
            'bar: Bar Graph\n\t\t' \
            'scatter: Scatter Graph\n\t\t' \
            'single_value: Single Value\n\t\t' \
            'table: Table'

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))

if DISCORD_BOT_TOKEN is None:
    raise EnvironmentError('Set Environment variable: DISCORD_BOT_TOKEN')
if GUILD_ID is None:
    raise EnvironmentError('Set Environment variable: GUILD_ID')


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


def is_numeric(text: str):
    try:
        int(text)
        return True
    except:
        return False


class DiscordController(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user or not message.content.startswith('!'):
            return
        channel = client.get_channel(message.channel.id)
        command = Command(command=message.content)
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

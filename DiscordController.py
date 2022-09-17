import asyncio
import functools
import os
import typing

import discord

import DuneApiConnector
import OutputFileCreator

COMMAND_OPTIONS = ['dune', 'help']
OUTPUT_OPTION_TYPES = ['bar', 'line', 'scatter', 'table']
HELP_TEXT = 'Commands: !dune QUERY_ID + (RESULT_TYPE)\n\t' \
            'QUERY_ID: Dune Query ID\n\t' \
            'RESUlT_TYPE: Optional parameter to define result type. Options:\n\t\t' \
            'line: Line Graph\n\t\t' \
            'bar: Bar Graph\n\t\t' \
            'scatter: Scatter Graph\n\t\t' \
            'table: Table'

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))


def to_thread(func: typing.Callable) -> typing.Coroutine:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        return await asyncio.to_thread(func, *args, **kwargs)

    return wrapper


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        if message.author == client.user or not message.content.startswith('!'):
            return
        channel = client.get_channel(message.channel.id)
        command = message.content[1:]
        command_correct = self.check_command(command=command)
        if not command_correct:
            await channel.send(HELP_TEXT)
            return
        ARGS = command.split(' ')
        await self.process_command(ARGS=ARGS, channel=channel)

    async def process_command(self, ARGS, channel):
        command = ARGS[0].lower()
        if command == 'dune':
            output_type = None
            if len(ARGS) == 3:
                output_type = ARGS[2]
            await channel.send(f'Executing Dune Query with ID: {ARGS[1]}')
            name = await self.process_dune_command(query_id=ARGS[1], output_type=output_type)
            if name is None:
                await channel.send('Query Failed')
            else:
                await channel.send(file=discord.File(name))
                os.remove(name)
        else:
            raise Exception()

    @to_thread
    def process_dune_command(self, query_id, output_type=None):
        data = DuneApiConnector.get_query_content(query_id)
        if data is None:
            return None
        name = None
        if output_type is None:
            pass
            # todo add default type
        else:
            output_type = output_type.lower()
            if output_type == 'bar':
                name = OutputFileCreator.plot_and_save_bar(data, query_id)
            elif output_type == 'line':
                name = OutputFileCreator.plot_and_save_line(data, query_id)
            elif output_type == 'scatter':
                name = OutputFileCreator.plot_and_save_scatter(data, query_id)
            elif output_type == 'table':
                name = OutputFileCreator.create_and_save_table(data, query_id)
            else:
                raise Exception
        return name

    def check_command(self, command):
        if command is None or command == '':
            return False
        split_command = command.split(' ')
        command = split_command[0].lower()
        if command not in COMMAND_OPTIONS:
            return False
        if command == 'help':
            # Help prints same output as error
            return False
        if len(split_command) < 2:
            return False
        try:
            int(split_command[1])
        except:
            return False
        if len(split_command) == 3:
            output_type = split_command[2].lower()
            if output_type not in OUTPUT_OPTION_TYPES:
                return False
        return True


if __name__ == '__main__':
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(DISCORD_BOT_TOKEN)

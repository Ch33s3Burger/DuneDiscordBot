import asyncio
import functools
import os
import typing

import discord

import formatting
import queries

TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILDID'))

print(TOKEN, GUILD_ID)


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
        channel_id = message.channel.id
        channel = client.get_channel(channel_id)
        text = message.content[1:]
        command_correct = self.check_command(text=text)
        if not command_correct:
            await channel.send(f'Commands: !dune QUERY_ID + (RESULT_TYPE)\n\t'
                               f'QUERY_ID: Dune Query ID\n\t'
                               f'RESUlT_TYPE: Optional parameter to define result type. Options:\n\t\t'
                               f'line: Line Graph\n\t\t'
                               f'bar: Bar Graph\n\t\t'
                               f'scatter: Scatter Graph\n\t\t'
                               f'table: Table')
            return
        ARGS = text.split(' ')
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
        data = queries.get_query_content(query_id)
        if data is None:
            return None
        name = None
        if output_type is None:
            pass
        else:
            output_type = output_type.lower()
            if output_type == 'bar':
                name = formatting.plot_and_save_bar(data, query_id)
            elif output_type == 'line':
                name = formatting.plot_and_save_line(data, query_id)
            elif output_type == 'scatter':
                name = formatting.plot_and_save_scatter(data, query_id)
            elif output_type == 'table':
                name = self.process_table(data, query_id)
            else:
                raise Exception
        return name

    def process_table(self, data, query_id):
        name = query_id + '_table.csv'
        data.to_csv(name)
        return name

    def check_command(self, text):
        if text is None or text == '':
            return False
        split_text = text.split(' ')
        command = split_text[0].lower()
        if command not in ['dune', 'help']:
            return False
        if command == 'help':
            return False
        if len(split_text) < 2:
            return False
        try:
            int(split_text[1])
        except:
            return False
        if len(split_text) == 3:
            output_type = split_text[2].lower()
            if output_type not in ['bar', 'line', 'scatter', 'table']:
                return False
        return True


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

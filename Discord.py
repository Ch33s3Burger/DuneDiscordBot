import os

import discord

import formatting
import queries

TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILDID'))

print(TOKEN, GUILD_ID)


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
                               f'plot: Line Graph\n\t\t'
                               f'bar: Bar Graph\n\t\t'
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
            await self.process_dune_command(query_id=ARGS[1], channel=channel, output_type=output_type)
        else:
            raise Exception()

    async def process_dune_command(self, query_id, channel, output_type=None):
        data = queries.get_query_content(query_id)
        if data is None:
            await channel.send('Query Failed')
            return
        if output_type is None:
            pass
        else:
            if output_type == 'bar':
                name = await formatting.plot_and_save_bar(data)
            elif output_type == 'plot':
                name = formatting.plot_and_save_line(data)
            elif output_type == 'scatter':
                name = await formatting.plot_and_save_scatter(data)
            elif output_type == 'table':
                name = self.process_table(data)
            else:
                raise Exception
        with open(name, 'rb') as file:
            await channel.send(file=discord.File(file))


    def process_table(self, data, channel):
        pass

    def process_plot(self, data, channel):
        pass

    def process_bar(self, data, channel):
        pass

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
        if len(split_text) == 3:
            output_type = split_text[2]
            if output_type not in ['bar', 'plot', 'scatter', 'table']:
                return False
        return True


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)

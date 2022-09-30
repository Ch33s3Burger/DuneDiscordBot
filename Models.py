import os

import discord
import numpy as np
import pandas as pd

import DuneApiConnector
from OutputTypeCreator import plot_and_save_by_type, create_and_save_table
from Cache import DuneQueryCache

PREFIX = '!'
COMMANDS_LIST = ['dune', 'help']
OUTPUT_TYPE_LIST = ['bar', 'line', 'scatter', 'table', 'single_value']
OUTPUT_TYPE_PLOT_LIST = ['bar', 'line', 'scatter']

HELP_TEXT_COMMAND = "!dune {dune_query_id} {output_type} {x_column} {y_column}\n"
HELP_TEXT_DUNE_QUERY_ID = 'ID of a Dune Query.'
HELP_TEXT_OUTPUT_TYPE = '(optional) Which result type the data should be given back.\n' \
                        '> bar: Matplotlib Bar graph\n' \
                        '> line: Matplotlib Line graph\n' \
                        '> scatter: Matplotlib Scatter graph\n' \
                        '> table: data as ".csv" table\n' \
                        '> single_value: Single value as text\n'
HELP_TEXT_X_COLUMN = '(optional) Name or index of the column to use for the x axis'
HELP_TEXT_Y_COLUMN = '(optional) Name or index of the column to use for the y axis'


def get_help_text_embed():
    embed = discord.Embed(title=HELP_TEXT_COMMAND)
    embed.add_field(name='dune_query_id', value=HELP_TEXT_DUNE_QUERY_ID, inline=False)
    embed.add_field(name='output_type', value=HELP_TEXT_OUTPUT_TYPE, inline=False)
    embed.add_field(name='x_column', value=HELP_TEXT_X_COLUMN, inline=False)
    embed.add_field(name='y_column', value=HELP_TEXT_Y_COLUMN, inline=False)
    embed.colour = discord.Color.blue()
    return embed


async def check_and_get_column_name(channel, data, column_name):
    if isinstance(column_name, str):
        if column_name.isnumeric():
            column_index = int(column_name)
            if column_index < 0 or column_index >= len(data.columns):
                await channel.send(f'Index {column_index} is out of bounds. Only found {len(data.columns)} columns.')
                return None
            return data.columns[column_index]
        if column_name not in data.columns:
            await channel.send(
                f'Column {column_name} does not exist. Continuing without specified column. Available columns are {data.columns}')
            return None
    return column_name


class Command:

    def __init__(self, command: str, cache: DuneQueryCache):
        self.command = command
        self.main_command = None
        self.dune_query_id = None
        self.output_type = None
        self.x_column_name = None
        self.y_column_name = None
        self.cache = cache

    def validate_command(self):
        if not self.command.startswith(PREFIX):
            return f'Command does not start with {PREFIX}'
        sub_commands = self.command[1:].lower().split(' ')
        if len(sub_commands) == 0:
            return 'Command missing. Type "!help" for more information.'
        main_command = sub_commands[0]
        if main_command in COMMANDS_LIST:
            self.main_command = main_command
        else:
            return f'Unknown Command {main_command}. Available Commands: {COMMANDS_LIST}.'
        if main_command == 'dune':
            return self.validate_dune_command(sub_commands[1:])
        return None

    def validate_dune_command(self, dune_commands: list):
        if len(dune_commands) == 0:
            return 'Missing Dune Query ID.'
        self.dune_query_id = dune_commands[0]
        if len(dune_commands) >= 2:
            output_type = dune_commands[1]
            if output_type in OUTPUT_TYPE_LIST:
                self.output_type = output_type
            else:
                return f'Unknown Output Type {output_type}. Available Output Types: {OUTPUT_TYPE_LIST}.'
            if output_type in OUTPUT_TYPE_PLOT_LIST:
                if len(dune_commands) >= 3:
                    self.x_column_name = dune_commands[2]
                if len(dune_commands) >= 4:
                    self.y_column_name = dune_commands[3]
        return None

    async def execute_command(self, channel):
        if self.main_command == 'help':
            await channel.send(embed=get_help_text_embed())
        elif self.main_command == 'dune':
            await self.execute_dune_command(channel)

    async def execute_dune_command(self, channel):
        data = None
        if self.cache.is_in_cache(self.dune_query_id):
            data = self.cache.get_from_cache(self.dune_query_id)
        if data is None:
            await channel.send(f'Executing Dune Query with ID: {self.dune_query_id}')
            data = await DuneApiConnector.get_query_content(self.dune_query_id)
            if data is None or isinstance(data, str):
                await channel.send(f'Error Message: {data}')
                return
            self.cache.add_to_cache(self.dune_query_id, data)
        self.x_column_name = await check_and_get_column_name(channel, data, self.x_column_name)
        self.y_column_name = await check_and_get_column_name(channel, data, self.y_column_name)
        if self.output_type is None:
            await self.set_suited_output_type(data)
        if self.output_type in OUTPUT_TYPE_PLOT_LIST:
            await self.create_and_send_plot(data, channel)
        elif self.output_type == 'table':
            await self.create_and_send_table(data, channel)
        elif self.output_type == 'single_value':
            await self.send_single_value(data, channel)
        else:
            channel.send(f'No suited output_type found. Pls specify')

    async def set_suited_output_type(self, data):
        num_rows, num_columns = data.shape
        if num_rows == 1:
            if num_columns == 1:
                self.output_type = 'single_value'
            else:
                self.output_type = 'table'
        elif num_rows > 1:
            self.output_type = 'line'

    async def create_and_send_plot(self, data, channel):
        x, y = await self.get_x_and_y_from_dataframe(data, channel)
        if x is None or y is None:
            return
        title = f'Dune Query ID: {self.dune_query_id}'
        file_name = plot_and_save_by_type(self.output_type, x, y, self.x_column_name, self.y_column_name, title)
        await channel.send(file=discord.File(file_name))
        os.remove(file_name)

    async def create_and_send_table(self, data, channel):
        file_name = create_and_save_table(data, self.dune_query_id)
        await channel.send(file=discord.File(file_name))
        os.remove(file_name)

    async def send_single_value(self, data, channel):
        num_rows, num_columns = data.shape
        if num_columns != 1 or num_rows != 1:
            await channel.send(f'Multiple Row/Columns found for output_type single value. Creating table instead.')
            await self.create_and_send_table(data, channel)
        else:
            await channel.send(f'Query returned single value: {data[0][0]}')

    async def get_x_and_y_from_dataframe(self, data: pd.DataFrame, channel):
        num_rows, num_columns = data.shape
        if num_columns == 0 or num_rows == 0:
            await channel.send('Query returned empty table.')
            return None, None
        if num_columns == 1:
            if num_rows == 1:
                await channel.send(f'Query returned single value: {data[0][0]}')
                return None, None
            else:
                return np.arrange(num_rows), data[0]
        elif num_columns >= 2:
            if self.x_column_name is None:
                datetime_column = self.get_datetime_column_if_exits(data)
                if datetime_column is None:
                    if self.y_column_name is None:
                        self.x_column_name = data.columns[0]  # first column
                    else:
                        column_names = data.columns
                        column_names_without_y_column = column_names[column_names != self.y_column_name]
                        self.x_column_name = column_names_without_y_column[0]
                else:
                    self.x_column_name = datetime_column
            if self.y_column_name is None:
                column_names = data.columns
                column_names_without_x = column_names[column_names != self.x_column_name]
                if len(column_names_without_x) > 1:
                    await channel.send(
                        'Multiple options found for y axis. Taking available first column. To change the y axis adjust your parameters.')
                self.y_column_name = column_names_without_x[0]
        return await self.get_x_and_y(data)

    async def get_x_and_y(self, data):
        if data[self.x_column_name].dtype == 'O':
            try:
                data[self.x_column_name] = pd.to_datetime(data[self.x_column_name])
            except:
                pass
        if data[self.y_column_name].dtype == 'O':
            try:
                data[self.y_column_name] = pd.to_datetime(data[self.y_column_name])
            except:
                pass
        data = data.sort_values([self.x_column_name])
        x = data[self.x_column_name]
        y = data[self.y_column_name]
        return x, y

    def get_datetime_column_if_exits(self, data):
        datetime_column = None
        column_names = data.columns
        column_names = column_names[column_names != self.y_column_name]
        for column_name in column_names:
            if data[column_name].dtype == 'O':
                try:
                    data[column_name] = pd.to_datetime(data[column_name])
                    datetime_column = column_name
                except:
                    pass
        return datetime_column

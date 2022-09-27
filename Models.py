import os
import threading

import discord
import numpy as np
import pandas as pd

import DuneApiConnector
from OutputFileCreator import plot_and_save_by_type, create_and_save_table

PREFIX = '!'
COMMANDS_LIST = ['dune', 'help']
OUTPUT_TYPE_LIST = ['bar', 'line', 'scatter', 'table', 'single_value']
OUTPUT_TYPE_PLOT_LIST = ['bar', 'line', 'scatter']
HELP_TEXT = 'HELP'


class Command:

    def __init__(self, command: str):
        self.command = command
        self.main_command = None
        self.dune_query_id = None
        self.output_type = None
        self.x_column_name: str = None
        self.y_column_name = None

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
                if len(dune_commands) == 4:
                    self.y_column_name = dune_commands[3]
        return None

    async def execute_command(self, channel):
        if self.main_command == 'help':
            channel.send(HELP_TEXT)
        elif self.main_command == 'dune':
            await self.execute_dune_command(channel)

    async def execute_dune_command(self, channel):
        await channel.send(f'Executing Dune Query with ID: {self.dune_query_id}')
        data = await DuneApiConnector.get_query_content(self.dune_query_id)
        if self.output_type is not None:
            if self.output_type in OUTPUT_TYPE_PLOT_LIST:
                await self.create_and_send_plot(data, channel)
            if self.output_type == 'table':
                await self.create_and_send_table(data, channel)
            elif self.output_type == 'single_value':
                await self.send_single_value(data, channel)
        else:
            pass
            # todo ask for more input or default

    async def create_and_send_plot(self, data, channel):
        x, y = await self.get_x_and_y_from_dataframe(data, channel)
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
            return None
        if num_columns == 1:
            if num_rows == 1:
                await channel.send(f'Query returned single value: {data[0][0]}')
                return None
            else:
                return np.arrange(num_rows), data[0]
        elif num_columns >= 2:
            if self.x_column_name is None:
                datetime_column = self.get_datetime_column_if_exits(data)
                if datetime_column is None:
                    if self.y_column_name is None:
                        self.x_column_name = 0 # first column
                    else:
                        column_names = data.columns
                        column_names_without_y = column_names[column_names != self.y_column_name]
                        self.x_column_name = column_names_without_y[0]
                else:
                    self.x_column_name = datetime_column
            if self.y_column_name is None:
                column_names_without_x = data.columns
                column_names_without_x = column_names_without_x[column_names_without_x != self.x_column_name]
                if len(column_names_without_x) > 1:
                    await channel.send('Multiple options found for y axis. Taking available first column. To change the y axis adjust your parameters.')
                self.y_column_name = column_names_without_x[0]
        return await self.get_x_and_y(channel, data)

    async def get_x_and_y(self, channel, data):
        x = y = None
        if self.x_column_name.isnumeric():
            self.x_column_name = int(self.x_column_name)
            data = data.sort_values([data.columns[self.x_column_name]])
            x = data.iloc[:, self.x_column_name]
        elif self.x_column_name in data.columns:
            data = data.sort_values([self.x_column_name])
            x = data[self.x_column_name]
        else:
            await channel.send(f'Column or column index {self.x_column_name} does not exist.')
        if self.y_column_name.isnumeric():
            self.y_column_name = int(self.y_column_name)
            y = data.iloc[:, self.y_column_name]
        elif self.y_column_name in data.columns:
            y = data[self.y_column_name]
        else:
            await channel.send(f'Column or column index {self.y_column_name} does not exist.')
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
                    print('failed to transform object to datetime')
        return datetime_column


if __name__ == '__main__':
    c = Command('!help')
    assert c.validate_command() is None
    c.execute_command()
    c = Command('!dune')
    assert c.validate_command() == 'Missing Dune Query ID.'
    c = Command('!dune 12345')
    assert c.validate_command() is None
    c = Command('!dune 12345 5')
    assert c.validate_command() == "Unknown Output Type 5. Available Output Types: ['bar', 'line', 'scatter', 'table', 'single_value']."
    c = Command('!dune 12345 bar')
    assert c.validate_command() is None
    c = Command('!dune 12345 bar 5')
    assert c.validate_command() is None
    c = Command('!dune 12345 bar 0 1')
    assert c.validate_command() is None

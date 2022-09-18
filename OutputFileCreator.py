"""
Created on Sat Sep 17 14:23:19 2022

@author: Lorenz
"""

import matplotlib.pyplot as plt
import pandas as pd


def df_columns_to_dt(df):
    datetime_column = None
    for column_name in df.columns:
        if df[column_name].dtype == 'O':
            try:
                df[column_name] = pd.to_datetime(df[column_name])
                datetime_column = column_name
            except:
                print('failed to transform object to datetime')
    return df, datetime_column


# send df and recieve name of file
def plot_and_save_line(df, query_id, title='Dune.com'):
    x, y = get_x_and_y_columns(df)

    fig, ax = plt.subplots()
    plt.plot(df[x], df[y])
    plt.xlabel(x)
    plt.ylabel(y)

    name = query_id + '_line.png'
    set_plot_settings_and_save_image(fig, name, title=title)
    return name


def plot_and_save_bar(df, query_id, title='Dune.com'):
    x, y = get_x_and_y_columns(df)

    fig, ax = plt.subplots()
    plt.bar(df[x], df[y], width=2.3)
    plt.xlabel(x)
    plt.ylabel(y)

    name = query_id + '_bar.png'
    set_plot_settings_and_save_image(fig, name, title=title)
    plt.xticks(x, rotation=45)
    return name


def plot_and_save_scatter(df, query_id, title='Dune.com'):
    x, y = get_x_and_y_columns(df)

    fig, ax = plt.subplots()
    plt.scatter(df[x], df[y])
    plt.xlabel(x)
    plt.ylabel(y)

    name = query_id + '_scatter.png'
    set_plot_settings_and_save_image(fig, name, title=title)
    return name


def get_x_and_y_columns(df):
    df, datetime_column = df_columns_to_dt(df)

    other_columns = df.columns[df.columns != datetime_column]
    if len(datetime_column) >= 1:
        y_column = other_columns[0]
    else:
        raise Exception('Only one column or only Datetime columns found')

    return datetime_column, y_column


def set_plot_settings_and_save_image(fig, name, title):
    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=8)
    plt.xticks(rotation=45)
    fig.tight_layout()
    plt.title(title)

    s = fig.get_size_inches() * fig.dpi
    logo = plt.imread('dune.jpg')
    fig.figimage(logo, s[0] / 2 - 40, s[1] / 2 - 30, alpha=.3, zorder=1)
    plt.savefig(name)


def create_and_save_table(data, query_id):
    name = query_id + '_table.csv'
    data.to_csv(name)
    return name

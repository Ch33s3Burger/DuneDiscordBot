# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 14:23:19 2022

@author: Lorenz
"""

from table2ascii import table2ascii, Alignment


def df_to_ascii(df):
    a = []
    for typ in df.dtypes.tolist():
        if typ == 'float64':
            a.append(Alignment.LEFT)
        elif typ == 'O':
            a.append(Alignment.CENTER)
        else:
            a.append(Alignment.RIGHT)

    output = table2ascii(
        header=list(df),
        body=df.values.tolist(),
        alignments=a)

    return output


import matplotlib.pyplot as plt
import time


# send df and recieve name of file
def plot_and_save_line(df, query_id, title='Dune.com'):
    fig, ax = plt.subplots()
    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=10)
    plt.plot(df.iloc[:, 0], df.iloc[:, 1])
    plt.xlabel(list(df)[1])
    plt.ylabel(list(df)[0])
    plt.title(title)

    s = fig.get_size_inches() * fig.dpi
    logo = plt.imread('dune.jpg')
    fig.figimage(logo, s[0] / 2 - 40, s[1] / 2 - 30, alpha=.3, zorder=1)

    name = query_id + '_line.png'
    plt.savefig(name)

    return name


def plot_and_save_bar(df, query_id, title='Dune.com'):
    fig, ax = plt.subplots()
    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=10)
    plt.bar(df.iloc[:, 0], df.iloc[:, 1])
    plt.xlabel(list(df)[1])
    plt.ylabel(list(df)[0])
    plt.title(title)

    s = fig.get_size_inches() * fig.dpi
    logo = plt.imread('dune.jpg')
    fig.figimage(logo, s[0] / 2 - 40, s[1] / 2 - 30, alpha=.3, zorder=1)

    name = query_id + '_bar.png'
    plt.savefig(name)

    return name


def plot_and_save_scatter(df, query_id, title='Dune.com'):
    fig, ax = plt.subplots()
    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=10)
    plt.scatter(df.iloc[:, 0], df.iloc[:, 1])
    plt.xlabel(list(df)[1])
    plt.ylabel(list(df)[0])
    plt.title(title)

    s = fig.get_size_inches() * fig.dpi
    logo = plt.imread('dune.jpg')
    fig.figimage(logo, s[0] / 2 - 40, s[1] / 2 - 30, alpha=.3, zorder=1)

    name = query_id + '_scatter.png'
    plt.savefig(name)

    return name

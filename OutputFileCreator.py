"""
Created on Sat Sep 17 14:23:19 2022

@author: Lorenz
"""

import matplotlib.pyplot as plt
import pandas as pd


def plot_and_save_by_type(type, x, y, x_label, y_label, title):
    fig, ax = plt.subplots()
    if type == 'bar':
        plt.bar(x, y)
    elif type == 'scatter':
        plt.scatter(x, y)
    elif type == 'line':
        plt.plot(x, y)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)

    name = title + '_line.png'
    set_plot_settings_and_save_image(fig, name, title=title)
    return name


def set_plot_settings_and_save_image(fig, name, title):
    plt.locator_params(axis='y', nbins=6)
    plt.locator_params(axis='x', nbins=8)
    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.25)
    plt.title(title)

    s = fig.get_size_inches() * fig.dpi
    logo = plt.imread('dune.jpg')
    fig.figimage(logo, s[0] / 2 - 40, s[1] / 2 - 30, alpha=.3, zorder=1)
    plt.savefig(name)


def create_and_save_table(data, query_id):
    name = query_id + '_table.csv'
    data.to_csv(name)
    return name

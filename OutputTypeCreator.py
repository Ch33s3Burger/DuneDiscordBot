"""
Created on Sat Sep 17 14:23:19 2022

@author: Lorenz
"""

import matplotlib.pyplot as plt


def plot_and_save_by_type(output_type, x, y, x_label, y_label, title):
    fig, ax = plt.subplots()
    if output_type == 'bar':
        plt.bar(x, y)
    elif output_type == 'scatter':
        plt.scatter(x, y)
    elif output_type == 'line':
        plt.plot(x, y)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)

    plt.xticks(rotation=45)
    plt.subplots_adjust(bottom=0.25)
    plt.title(title)

    # print dune logo in plot
    s = fig.get_size_inches() * fig.dpi
    logo = plt.imread('dune.jpg')
    fig.figimage(logo, s[0] / 2 - 40, s[1] / 2 - 30, alpha=.3, zorder=1)

    # save image as png
    name = f'{title}_{output_type}.png'
    plt.savefig(name)
    return name


def create_and_save_table(data, query_id):
    name = query_id + '_table.csv'
    data.to_csv(name)
    return name

"""
Author: Ben Kruse
Date: 1/25/2022
File: tree-ring-cs-opener.py
Description: Takes a CSV of tree ring data and plots the data,
the program also prints to the terminal many characteristics of the data
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys


def calc_avg_length(data):
    """ Calculates the average length of many time series
    :param data: a DataFrame containing the time series
    :return: the average length of the time series
    """
    assert type(data) is pd.DataFrame
    out = 0.0
    for series_name in data:
        series = data[series_name]
        first = series.first_valid_index()
        last = series.last_valid_index()
        # Add the length of every series
        out += last - first + 1
    return round(out/len(data.columns), 1)  # Return their average


def read_csv():
    """ reads a given CSV and returns the corresponding DataFrame
    :return: the DataFrame
    """
    if len(sys.argv) != 2:
        print("Please enter a file name for the program")
        return
    filename = sys.argv[1]
    tree_data = pd.read_csv(filename)
    tree_data.set_index("Year", inplace=True)
    return tree_data


def print_info(tree_data):
    """ Prints off various bits of information about a tree ring dataset
    :param tree_data: A DataFrame with the tree ring data
    :return: None
    """
    print("Number of dated series:", len(tree_data.columns))
    print("Total number of measurements:", tree_data.count().sum())
    print("Average series length:", calc_avg_length(tree_data))
    print("Range:", tree_data.shape[0])
    print("Span:", tree_data.first_valid_index(), "-", tree_data.last_valid_index())
    # printing off the missing data for each series
    print("Years with missing data for each time-series:")
    for series_name in tree_data:
        series = tree_data[series_name]
        # Get the first and last year for each series that has data
        first = series.first_valid_index()
        last = series.last_valid_index()
        # Takes all the years that have the value=0 (no data)
        zero_years = series.between(left=first, right=last)[series == 0]
        if len(zero_years) > 0:
            # Joins all the years in a readable format
            print(f'  {series_name}: {" ".join([str(year) for year in zero_years.keys()])}')


def graph(tree_data):
    """ Graphs a spaghetti plot of all the tree ring data
    :param tree_data: A DataFrame with the tree ring data
    :return: None
    """
    # This configures all the lines to share the same x-axis and have no
    # vertical padding
    fig, axs = plt.subplots(len(tree_data.columns), 1, sharex=True)
    fig.subplots_adjust(hspace=0)

    for i, series_name in enumerate(tree_data):
        series = tree_data[series_name]
        axs[i].axis("off")
        # This positions the title to the right side and scales it correctly
        # (-.02, 1.01)[i % 2] alternates between the two sides
        axs[i].set_title(series_name, y=-.3, x=(-.02, 1.01)[i % 2], fontsize=8)
        axs[i].plot(series.index, series)

    plt.show()


def main():
    tree_data = read_csv()
    print(tree_data.head(1))  # The required portion that prints the first line
    print_info(tree_data)
    graph(tree_data)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
""" Risk plot generator (rpg) """

import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import random

observation_names = []
amount_of_observations = []
risk_rating = []
x_coords = []
y_coords = []
amount_high = 0
amount_medium = 0
amount_low = 0

def get_args():
    """ Get arguments """
    parser = argparse.ArgumentParser(description='Converting scanning reports to a tabular format')
    parser.add_argument('-g', '--grid', action='store_true',
                        help='generate a risk grid.')
    parser.add_argument('-r', '--ring', action='store_true',
                        help='generate a risk ring.')
    parser.add_argument('-iC', '--input-csv-file', required=True,
                        help='specify an input CSV file (e.g. data.csv).')
    parser.add_argument('-oP', '--output-png-file',
                        help='specify an output PNG file (e.g. risk.png).')
    return parser.parse_args()

def load_csv(args):
    """ Import CSV and translate Likelihood and Impact to numbers """

    global amount_high
    global amount_medium
    global amount_low
    with open(args.input_csv_file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)
        for row in data:
            observation_names.append(row[0])
            risk_rating.append(row[3])
            if row[1] == "H":
                x = 450
            elif row[1] == "M":
                x = 300
            elif row[1] == "L":
                x = 150
            if row[2] == "H":
                y = 300
            elif row[2] == "M":
                y = 200
            elif row[2] == "L":
                y = 100
            if row[3] == "H":
                amount_high += 1
            elif row[3] == "M":
                amount_medium += 1
            elif row[3] == "L":
                amount_low += 1
            x_coords.append(x)
            y_coords.append(y)

    for row in enumerate(observation_names):
        amount_of_observations.append(row[0])

def ring(args):
    """ Ring functions """
    fig, ax = plt.subplots(subplot_kw=dict(aspect="equal"))

    # Ring width size
    size = 0.25

    data = amount_high, amount_medium, amount_low
    labels = ["High", "Medium", "Low"]
    colors = ["red", "orange", "yellow"]

    # Plot wedges
    ax.pie(data, wedgeprops=dict(width=size, edgecolor="black", linewidth=1), startangle=90,
           colors=colors, labels=data)

    # Determine exposure_level
    largest_index = data.index(max(data))
    if largest_index == 0:
        exposure_level = "High"
    elif largest_index == 1:
        exposure_level = "Medium"
    elif largest_index == 2:
        exposure_level = "Low"

    # Print exposure level
    ax.text(0.5, 0.5, "Exposure level", transform=ax.transAxes, fontsize=10,
            horizontalalignment='center', verticalalignment='center')
    ax.text(0.5, 0.43, exposure_level, transform=ax.transAxes, fontsize=14,
            horizontalalignment='center', verticalalignment='center')

    # Print legend
    ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)

    # Output
    if not args.output_png_file:
        plt.show()
    else:
        plt.savefig(args.output_png_file, transparent=True, dpi=200, bbox_inches='tight')

def grid(args):
    """ Grid function """

    # Background
    img = plt.imread("data/bg.png")

    # Axis spacing values
    x_axis_spacing = plticker.MultipleLocator(base=150)
    y_axis_spacing = plticker.MultipleLocator(base=100)

    # Some plot markers
    markers = ['o', 's', 'D', 'd', '^', '>', 'v', '<', '*', 'P', 'x', 'X', '|', '_', '1', '2', '3',
               '4']

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 450, 0, 300])

    # Plot observations with a random offset inside their quadrant
    for i, name, marker, risk in zip(amount_of_observations, observation_names, markers,
                                     risk_rating):
        x_random = random.randint(x_coords[i]-80, x_coords[i]-20)
        y_random = random.randint(y_coords[i]-80, y_coords[i]-20)
        x = x_random
        y = y_random
        if risk == 'H':
            ax.scatter(x, y, marker=marker, c='red')
        elif risk == 'M':
            ax.scatter(x, y, marker=marker, c='orange')
        elif risk == 'L':
            ax.scatter(x, y, marker=marker, c='green')
        # ax.text(x+0, y-15, name, fontsize=5, horizontalalignment='center')

    # Print legend
    ax.legend(observation_names, loc="upper left", ncol=1, bbox_to_anchor=(1, 1.02))

    # Hide axis numbers
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Grid spacing
    ax.xaxis.set_major_locator(x_axis_spacing)
    ax.yaxis.set_major_locator(y_axis_spacing)

    # Print arrows along axis
    ax.annotate('High', va="center", xy=(0, -0.07), xycoords='axes fraction', xytext=(1, -0.07),
                arrowprops=dict(arrowstyle="<-", color='black'))
    ax.annotate('High', ha="center", xy=(-0.05, 0), xycoords='axes fraction', xytext=(-0.05, 1),
                arrowprops=dict(arrowstyle="<-", color='black'))

    # Print axis titles
    plt.xlabel("Likelihood", labelpad=20)
    plt.ylabel("Impact", labelpad=20)

    # Print grid
    plt.grid(color='black', alpha=0.5, linestyle='--')

    # Output
    if not args.output_png_file:
        plt.show()
    else:
        plt.savefig(args.output_png_file, transparent=True, dpi=200, bbox_inches='tight')

args = get_args()
load_csv(args)
if args.ring:
    ring(args)
if args.grid:
    grid(args)

#!/usr/bin/env python3
""" Risk plot generator (rpg) """

import argparse
import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
import os
import random
from pathlib import Path

numbers = []
observation_names = []
amount_of_observations = []
risk_rating = []
mylabels = []
x_coords = []
y_coords = []
amount_high = 0
amount_medium = 0
amount_low = 0

def get_args():
    """ Get arguments """

    parser = argparse.ArgumentParser(description='Converting scanning reports to a tabular format')
    parser.add_argument('-g', '--grid', action='store_true',
                        help='generate a risk grid plot.')
    parser.add_argument('-d', '--donut', action='store_true',
                        help='generate a risk donut.')
    parser.add_argument('-r', '--recommendations', action='store_true',
                        help='generate a risk recommendations plot.')
    parser.add_argument('-iC', '--input-csv-file', required=True,
                        help='specify an input CSV file (e.g. data.csv).')
    parser.add_argument('-oP', '--output-png-file',
                        help='specify an output PNG file (e.g. risk.png).')
    parser.add_argument('--axis-labels',
                        help='specify to print the axis labels')
    parser.add_argument('--axis-arrows',
                        help='specify to print arrows along the axis')
    parser.add_argument('--legend',
                        help='specify to print the legend')
    return parser.parse_args()

def load_risk_csv(args):
    """ Import CSV and translate Likelihood and Impact to numbers """

    global amount_high
    global amount_medium
    global amount_low
    with open(args.input_csv_file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)
        for row in data:
            numbers.append(row[0])
            observation_names.append(row[1])
            risk_rating.append(row[4])
            if row[2] == "H":
                x = 450
            elif row[2] == "M":
                x = 300
            elif row[2] == "L":
                x = 150
            if row[3] == "H":
                y = 300
            elif row[3] == "M":
                y = 200
            elif row[3] == "L":
                y = 100
            if row[4] == "H":
                amount_high += 1
            elif row[4] == "M":
                amount_medium += 1
            elif row[4] == "L":
                amount_low += 1
            x_coords.append(x)
            y_coords.append(y)

    for row in enumerate(observation_names):
        amount_of_observations.append(row[0])

def load_recommendations_csv(args):
    """ Import CSV and translate Likelihood and Impact to numbers """

    with open(args.input_csv_file, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',')
        next(data)
        for row in data:
            numbers.append(row[0])
            observation_names.append(row[1])
            if row[2] == "H":
                x = 450
            elif row[2] == "M":
                x = 300
            elif row[2] == "L":
                x = 150
            if row[3] == "H":
                y = 300
            elif row[3] == "M":
                y = 200
            elif row[3] == "L":
                y = 100
            x_coords.append(x)
            y_coords.append(y)

    for row in enumerate(observation_names):
        amount_of_observations.append(row[0])

def donut(args):
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
    ax.text(0.5, 0.53, "Exposure level", transform=ax.transAxes, fontsize=16,
            horizontalalignment='center', verticalalignment='center')
    ax.text(0.5, 0.45, exposure_level, transform=ax.transAxes, fontsize=24,
            horizontalalignment='center', verticalalignment='center', weight='bold')

    # Print legend
    if args.legend:
        ax.legend(labels, loc="center left", bbox_to_anchor=(1, 0.5), ncol=1)

    # Output
    if not args.output_png_file:
        plt.show()
    else:
        plt.savefig(args.output_png_file, transparent=True, dpi=200, bbox_inches='tight')

def grid(args):
    """ Grid function """

    # Background
    bg = Path("data/grid-bg.png")
    if os.path.isfile(bg):
        img = plt.imread("data/grid-bg.png")
    else:
        img = plt.imread("/usr/share/rpg/data/grid-bg.png")

    # Axis spacing values
    x_axis_spacing = plticker.MultipleLocator(base=150)
    y_axis_spacing = plticker.MultipleLocator(base=100)

    # Some plot markers
    # markers = ['o', 's', 'D', 'd', '^', '>', 'v', '<', '*', 'P', 'x', 'X', '|', '_', '1', '2',
    #            '3', '4']

    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 450, 0, 300])

    # Plot observations with a random offset inside their quadrant
    for number, i, name, risk in zip(numbers, amount_of_observations, observation_names,
                                     risk_rating):
        #x_random = random.randint(x_coords[i]-90, x_coords[i]-10)
        #y_random = random.randint(y_coords[i]-90, y_coords[i]-10)
        x_random = random.randrange(x_coords[i]-90, x_coords[i]-10, 25)
        y_random = random.randrange(y_coords[i]-80, y_coords[i]-10, 20)
        x = x_random
        y = y_random
        if risk == 'H':
            ax.scatter(x, y, marker='o', c='#e20000', s=200, edgecolors='black')
            ax.text(x+0, y-3, number, fontsize=7, horizontalalignment='center', color='white',
                    weight='bold')
        elif risk == 'M':
            ax.scatter(x, y, marker='o', c='#fecb00', s=200, edgecolors='black')
            ax.text(x+0, y-3, number, fontsize=7, horizontalalignment='center', color='white',
                    weight='bold')
        elif risk == 'L':
            ax.scatter(x, y, marker='o', c='#ffff00', s=200, edgecolors='black')
            ax.text(x+0, y-3, number, fontsize=7, horizontalalignment='center', color='black',
                    weight='bold')

    # Print legend
    if args.legend:
        for item in zip(numbers, observation_names):
            mylabels.append(' '.join(item))
        ax.legend(observation_names, labels=mylabels, loc="upper left", ncol=1,
                  bbox_to_anchor=(1, 1.02))

    # Hide axis numbers
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Grid spacing
    ax.xaxis.set_major_locator(x_axis_spacing)
    ax.yaxis.set_major_locator(y_axis_spacing)

    # Print arrows along axis
    if args.axis_arrows:
        ax.annotate('High', va="center", xy=(0, -0.07), xycoords='axes fraction', xytext=(1, -0.07),
                    arrowprops=dict(arrowstyle="<-", color='black'))
        ax.annotate('High', ha="center", xy=(-0.05, 0), xycoords='axes fraction', xytext=(-0.05, 1),
                    arrowprops=dict(arrowstyle="<-", color='black'))

    # Print axis labels
    if args.axis_labels:
        plt.xlabel("Likelihood", labelpad=20)
        plt.ylabel("Impact", labelpad=20)

    # Print grid
    plt.grid(color='black', alpha=0.5, linestyle='--')

    # Output
    if not args.output_png_file:
        plt.show()
    else:
        plt.savefig(args.output_png_file, transparent=True, dpi=200, bbox_inches='tight')

def recommendations(args):
    """ Grid function """

    # Background
    bg = Path("data/recommendations-bg.png")
    if os.path.isfile(bg):
        img = plt.imread("data/recommendations-bg.png")
    else:
        img = plt.imread("/usr/share/rpg/data/recommendations-bg.png")

    # Axis spacing values
    x_axis_spacing = plticker.MultipleLocator(base=150)
    y_axis_spacing = plticker.MultipleLocator(base=100)

    # Some plot markers
    # markers = ['o', 's', 'D', 'd', '^', '>', 'v', '<', '*', 'P', 'x', 'X', '|', '_', '1', '2',
    #            '3', '4']
    fig, ax = plt.subplots()
    ax.imshow(img, extent=[0, 450, 0, 300])

    # Plot observations with a random offset inside their quadrant
    for number, i, name in zip(numbers, amount_of_observations, observation_names):
		#x_random = random.randint(x_coords[i]-140, x_coords[i]-10)
        #y_random = random.randint(y_coords[i]-90, y_coords[i]-10)
        x_random = random.randrange(x_coords[i]-130, x_coords[i]-10, 25)
        y_random = random.randrange(y_coords[i]-80, y_coords[i]-10, 20)
        x = x_random
        y = y_random
        ax.scatter(x, y, marker='o', c='#4f81bd', s=250, edgecolors='black')
        ax.text(x+0, y-3, number, fontsize=6, horizontalalignment='center', color='white', weight='bold')

    # Print legend
    if args.legend:
        for item in zip(numbers, observation_names):
            mylabels.append(' '.join(item))
        ax.legend(observation_names, labels=mylabels, loc="upper left", ncol=1,
                  bbox_to_anchor=(1, 1.02))

    # Hide axis numbers
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    # Grid spacing
    ax.xaxis.set_major_locator(x_axis_spacing)
    ax.yaxis.set_major_locator(y_axis_spacing)

    # Print arrows along axis
    if args.axis_arrows:
        ax.annotate('High', va="center", xy=(0, -0.07), xycoords='axes fraction', xytext=(1, -0.07),
                    arrowprops=dict(arrowstyle="<-", color='black'))
        ax.annotate('High', ha="center", xy=(-0.05, 0), xycoords='axes fraction', xytext=(-0.05, 1),
                    arrowprops=dict(arrowstyle="<-", color='black'))

    # Print axis labels
    if args.axis_labels:
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

if args.donut or args.grid:
    load_risk_csv(args)
elif args.recommendations:
    load_recommendations_csv(args)

if args.donut:
    donut(args)
if args.grid:
    grid(args)
if args.recommendations:
    recommendations(args)

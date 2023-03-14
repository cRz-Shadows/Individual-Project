# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 23:21:51 2023

@author: craig
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
from math import pi
import json
import textwrap

# Define the data types for each column
team_dtypes = [('team', int), ('wins', int), ('losses', int), ('avg_switch', float),
          ('avg_ko', float), ('avg_fight', float), ('avg_weather_sand', float),
          ('avg_weather_hail', float), ('avg_weather_sun', float), ('avg_weather_rain', float), 
          ('battles', int)]

pokemon_dtypes = [('pokemon_number', int), ('kos', int), ('team_wins', int), ('top_100_appearences', int)]

# Load all the data 
win_loss_team = np.loadtxt('Outputs/Win_Loss_outputMatrix.txt', dtype=team_dtypes, skiprows=1)
quick_win_team = np.loadtxt('Outputs/Quick_Win_outputMatrix.txt', dtype=team_dtypes, skiprows=1)
switch_ins_team = np.loadtxt('Outputs/Switch_Ins_outputMatrix.txt', dtype=team_dtypes, skiprows=1)
weather_team = np.loadtxt('Outputs/Weather_outputMatrix.txt', dtype=team_dtypes, skiprows=1)
win_loss_pokemon = np.loadtxt('Outputs/Win_Loss_pokemonMatrix.txt', dtype=pokemon_dtypes, skiprows=1)
quick_win_pokemon = np.loadtxt('Outputs/Quick_Win_pokemonMatrix.txt', dtype=pokemon_dtypes, skiprows=1)
switch_ins_pokemon = np.loadtxt('Outputs/Switch_Ins_pokemonMatrix.txt', dtype=pokemon_dtypes, skiprows=1)
weather_pokemon = np.loadtxt('Outputs/Weather_pokemonMatrix.txt', dtype=pokemon_dtypes, skiprows=1)
item_dicts = []
ability_dicts = []
move_dicts = []
pokemon_numbers_dicts = []

models = ['Win_Loss', 'Quick_Win', 'Switch_Ins', 'Weather']
for model in models:
    with open('Outputs/' + model + '_itemDict.json', 'r') as f:
        item_dicts.append(json.load(f))
    with open('Outputs/' + model + '_abilityDict.json', 'r') as f:
        ability_dicts.append(json.load(f))
    with open('Outputs/' + model + '_moveDict.json', 'r') as f:
        move_dicts.append(json.load(f))
    with open('Outputs/' + model + '_pokemonNumbers.json', 'r') as f:
        pokemon_numbers_dicts.append(json.load(f))

team_matrices = [win_loss_team, quick_win_team, switch_ins_team, weather_team]
pokemon_matrices = [win_loss_pokemon, quick_win_pokemon, switch_ins_pokemon, weather_pokemon]

for n, data in enumerate(team_matrices):
    model = models[n].replace('_', '-')
    # Extract the data
    teams = data['team']
    wins = data['wins']
    losses = data['losses']
    avg_switch = data['avg_switch']
    avg_ko = data['avg_ko']
    avg_fight = data['avg_fight']
    avg_weather_sand = data['avg_weather_sand']
    avg_weather_hail = data['avg_weather_hail']
    avg_weather_sun = data['avg_weather_sun']
    avg_weather_rain = data['avg_weather_rain']
    
    total_games = wins + losses
    norm_wins = wins / total_games
    norm_losses = losses / total_games
    avg_weather = avg_weather_sand + avg_weather_hail + avg_weather_sun + avg_weather_rain
    prop_sand = avg_weather_sand / avg_weather
    prop_hail = avg_weather_hail / avg_weather
    prop_sun = avg_weather_sun / avg_weather
    prop_rain = avg_weather_rain / avg_weather
    
    # Bar chart of wins and losses for each team
    plt.bar(teams, norm_wins, label='Wins')
    plt.bar(teams, norm_losses, bottom=norm_wins, label='Losses')
    plt.xlabel('Team')
    plt.ylabel('Proportion of games won/lost')
    plt.title('Team Wins and Losses', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.legend()
    plt.show()
    
    plt.hist(avg_fight, bins=16, edgecolor='black')
    plt.xlabel('Average Length of Fight')
    plt.ylabel('Frequency')
    plt.title('Distribution of Average Length of Fight for a Single Team', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle('Win-Loss Synergys - Lower is Better', y=0.95, fontsize=12)
    plt.show()
    
    plt.hist(avg_weather, bins=16, edgecolor='black')
    plt.xlabel('Average Number of Weather Changes per Battle')
    plt.ylabel('Number of Teams')
    plt.title('Distribution of Average Number of Weather Changes per Battle for Each Team', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.show()
    
    plt.bar(teams, avg_weather, color='gray', edgecolor='gray')
    plt.bar(teams, avg_weather_sand, color='#ffcc99', edgecolor='#ffcc99')
    plt.bar(teams, avg_weather_hail, bottom=avg_weather_sand, color='lightgray', edgecolor='lightgray')
    plt.bar(teams, avg_weather_sun, bottom=avg_weather_sand+avg_weather_hail, color='red', edgecolor='red')
    plt.bar(teams, avg_weather_rain, bottom=avg_weather_sand+avg_weather_hail+avg_weather_sun, color='steelblue', edgecolor='steelblue')
    plt.xlabel('Team')
    plt.ylabel('Average Weather Changes')
    plt.title('Weather Averages for Each Team', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    sand_patch = plt.Rectangle((0, 0), 1, 1, color='#ffcc99')
    hail_patch = plt.Rectangle((0, 0), 1, 1, color='lightgray')
    sun_patch = plt.Rectangle((0, 0), 1, 1, color='red')
    rain_patch = plt.Rectangle((0, 0), 1, 1, color='steelblue')
    plt.legend([sand_patch, hail_patch, sun_patch, rain_patch], ['Sand', 'Hail', 'Sun', 'Rain'])
    plt.show()
    
    plt.hist(data['avg_switch'], bins=5, edgecolor='black')
    plt.xlabel('Average Number of Switches per Battle')
    plt.ylabel('Frequency')
    plt.title('Histogram of Average Number of Switches per Battle', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.show()
    
    break;
    
for n, data in enumerate(pokemon_matrices):
    model = models[n].replace('_', '-')
    pokemon_numbers = data['pokemon_number']
    kos = data['kos']
    wins = data['team_wins']
    top_100_appearences = data['top_100_appearences']

    distinct_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
    '#393b79', '#6b6ecf', '#9c9ede', '#cedb9c', '#8c6d31',
    '#bd9e39', '#e7ba52', '#843c39', '#ad494a', '#d6616b',
    '#e7969c', '#7b4173', '#a55194', '#ce6dbd', '#de9ed6',
    '#3182bd', '#6baed6', '#9ecae1', '#c6dbef', '#e6550d',
    '#fd8d3c', '#fdae6b', '#fdd0a2', '#31a354', '#74c476',
    '#a1d99b', '#c7e9c0', '#756bb1', '#9e9ac8', '#bcbddc',
    '#dadaeb', '#636363', '#969696', '#bdbdbd', '#d9d9d9',
    '#ffffff', '#000000'
    ]

    pokemonNumbers = pokemon_numbers_dicts[n]
    # Replace the Pokemon numbers with their names
    pokemon_names = [pokemonNumbers[str(num)] for num in pokemon_numbers]
    
    # Create the scatter plot
    fig, ax = plt.subplots()
    for i, name in enumerate(pokemon_names):
        color = distinct_colors[i % len(distinct_colors)]  # Cycle through colors if there are more points than colors
        ax.scatter(kos[i], wins[i], c=color, label=name)
    # Add the legend with the colors and labels
    ax2 = fig.add_axes([0.85, 0.1, 0.05, 0.8])
    for i, name in enumerate(pokemon_names):
        color = distinct_colors[i % len(distinct_colors)]
        ax2.scatter([0], [i], c=color, label=name)
    ax2.legend(loc='center left', bbox_to_anchor=(6.5, 0.5))
    ax2.set_axis_off()
    # Add axis labels and title
    ax.set_xlabel('Individual Pokemon KOs')
    ax.set_ylabel('Wins for the top performing team')
    ax.set_title('Relationship between Individual Pokemon KOs and Team Wins', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    # Show the plot
    plt.show()
    
    # pi chart
    # define your labels and sizes
    labels = [(pokemonNumbers[str(num)][0], pokemonNumbers[str(num)][1]) for num in data['pokemon_number']]
    sizes = top_100_appearences

    cmap = mcolors.ListedColormap(distinct_colors)
    
    # get the colors for each label
    colors = [cmap(i) for i in range(len(set(labels)))]
    
    # create the pie chart with the specified colors
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=None, colors=colors, autopct='%1.1f%%')
    ax.set_title('Percentage of Appearance of Each Pokemon on Top 100 Teams', y=1.1, fontsize=16, fontweight='bold')
    fig.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    legend = ax.legend(labels, loc='center left', bbox_to_anchor=(1.2, 0.5))
    legend.set_title('Pokemon')
    for i, text in enumerate(legend.get_texts()):
        text.set_color(colors[i])
    plt.show()
    
    
    sizes = kos
    # create the pie chart with the specified colors
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(sizes, labels=None, colors=colors, autopct='%1.1f%%')
    ax.set_title('Percentage of KOs for Each Pokemon', y=1.1, fontsize=16, fontweight='bold')
    legend = ax.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5))
    fig.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    legend.set_title('Pokemon')
    for i, text in enumerate(legend.get_texts()):
        text.set_color(colors[i])
    plt.show()
    
    break;
    
for data in move_dicts:
    model = models[n].replace('_', '-')
    # sort the dictionary by KOs in descending order and take the top 20 moves
    sorted_moves = sorted(data.items(), key=lambda x: x[1], reverse=True)[:20]
    
    # extract the move names and KOs as separate lists
    move_names = [move[0] for move in sorted_moves]
    ko_counts = [move[1] for move in sorted_moves]
    
    # create a bar chart of the top 20 moves
    plt.bar(move_names, ko_counts, edgecolor='black')
    plt.xticks(rotation=90)
    plt.xlabel('Moves')
    plt.ylabel('KOs')
    plt.title('Top 20 Pokemon Moves by KOs', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.show()
    break;
    
for data in ability_dicts:
    model = models[n].replace('_', '-')
    # sort the dictionary by KOs in descending order and take the top 20 moves
    sorted_abilities = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
    # extract the move names and KOs as separate lists
    ability_names = [name[0] for name in sorted_abilities]
    uses = [name[1] for name in sorted_abilities]
    
    # create a bar chart of the top 20 moves
    plt.bar(ability_names, uses, edgecolor='black')
    plt.xticks(rotation=90)
    plt.xlabel('Abilities')
    plt.ylabel('Uses In Top 100 Teams')
    plt.title('Ability Appearences In Top 100 Teams', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.show()
    break;
    
for data in item_dicts:
    model = models[n].replace('_', '-')
    # sort the dictionary by KOs in descending order and take the top 20 moves
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    
    # extract the move names and KOs as separate lists
    item_names = [name[0] for name in sorted_items]
    uses = [name[1] for name in sorted_items]
    
    # create a bar chart of the top 20 moves
    plt.bar(item_names, uses, edgecolor='black')
    plt.xticks(rotation=90)
    plt.xlabel('Items')
    plt.ylabel('Uses In Top 100 Teams')
    plt.title('Item Appearences In Top 100 Teams', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle(model + ' Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.show()
    break;

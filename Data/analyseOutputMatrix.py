# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 23:21:51 2023

@author: craig
"""

import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Define the data types for each column
dtypes = [('team', int), ('wins', int), ('losses', int), ('avg_switch', float),
          ('avg_ko', float), ('avg_fight', float), ('avg_weather_sand', float),
          ('avg_weather_hail', float), ('avg_weather_sun', float), ('avg_weather_rain', float), 
          ('battles', int)]

#--------------------------------------------------------------------------------------------------------------------
# Quick-Win

# Load the text file and skip the first row
win_loss_data = np.loadtxt('Outputs/Win_Loss_outputMatrix.txt', dtype=dtypes, skiprows=1)
quick_win_data = np.loadtxt('Outputs/Quick_Win_outputMatrix.txt', dtype=dtypes, skiprows=1)
switch_ins_data = np.loadtxt('Outputs/Switch_Ins_outputMatrix.txt', dtype=dtypes, skiprows=1)
weather_data = np.loadtxt('Outputs/Weather_outputMatrix.txt', dtype=dtypes, skiprows=1)
matrices = [win_loss_data, quick_win_data, switch_ins_data, weather_data]

for data in matrices:
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
    plt.suptitle('Win-Loss Synergys - Higher is Better', y=0.95, fontsize=12)
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
    plt.suptitle('Switch-In Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.show()
    
    plt.bar(teams, avg_weather, color='gray', edgecolor='gray')
    plt.bar(teams, avg_weather_sand, color='#ffcc99', edgecolor='#ffcc99')
    plt.bar(teams, avg_weather_hail, bottom=avg_weather_sand, color='lightgray', edgecolor='lightgray')
    plt.bar(teams, avg_weather_sun, bottom=avg_weather_sand+avg_weather_hail, color='#ffad33', edgecolor='#ffad33')
    plt.bar(teams, avg_weather_rain, bottom=avg_weather_sand+avg_weather_hail+avg_weather_sun, color='steelblue', edgecolor='steelblue')
    plt.xlabel('Team')
    plt.ylabel('Average Weather Changes')
    plt.title('Weather Averages for Each Team', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle('Weather Type Distribution', y=0.95, fontsize=12)
    sand_patch = plt.Rectangle((0, 0), 1, 1, color='#ffcc99')
    hail_patch = plt.Rectangle((0, 0), 1, 1, color='lightgray')
    sun_patch = plt.Rectangle((0, 0), 1, 1, color='#ffad33')
    rain_patch = plt.Rectangle((0, 0), 1, 1, color='steelblue')
    plt.legend([sand_patch, hail_patch, sun_patch, rain_patch], ['Sand', 'Hail', 'Sun', 'Rain'])
    plt.show()
    
    plt.hist(data['avg_switch'], bins=5, edgecolor='black')
    plt.xlabel('Average Number of Switches per Battle')
    plt.ylabel('Frequency')
    plt.title('Histogram of Average Number of Switches per Battle', y=1.1, fontsize=16, fontweight='bold')
    plt.suptitle('Win-Loss Synergys - Higher is Better', y=0.95, fontsize=12)
    plt.show()

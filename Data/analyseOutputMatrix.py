# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 23:21:51 2023

@author: craig
"""

import numpy as np
import matplotlib.pyplot as plt
from math import pi

# Define the data types for each column
dtypes = [('team', int), ('wins', int), ('losses', int), ('avg_switch', float), ('avg_ko', float), ('avg_fight', float), ('avg_weather', float), ('battles', int)]

#--------------------------------------------------------------------------------------------------------------------
# Win-Loss

# Load the text file and skip the first row
data = np.loadtxt('Outputs/Win_Loss_outputMatrix.txt', dtype=dtypes, skiprows=1)

# Extract the data
teams = data['team']
wins = data['wins']
losses = data['losses']
avg_switch = data['avg_switch']
avg_ko = data['avg_ko']
avg_fight = data['avg_fight']
avg_weather = data['avg_weather']

total_games = wins + losses
norm_wins = wins / total_games
norm_losses = losses / total_games

# Bar chart of wins and losses for each team
plt.bar(teams, norm_wins, label='Wins')
plt.bar(teams, norm_losses, bottom=norm_wins, label='Losses')
# Add a subheading
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
plt.suptitle('Win-Loss Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()

plt.hist(data['avg_switch'], bins=5, edgecolor='black')
plt.xlabel('Average Number of Switches per Battle')
plt.ylabel('Frequency')
plt.title('Histogram of Average Number of Switches per Battle', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Win-Loss Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()


#--------------------------------------------------------------------------------------------------------------------
# Quick-Win

# Load the text file and skip the first row
data = np.loadtxt('Outputs/Quick_Win_outputMatrix.txt', dtype=dtypes, skiprows=1)

# Extract the data
teams = data['team']
wins = data['wins']
losses = data['losses']
avg_switch = data['avg_switch']
avg_ko = data['avg_ko']
avg_fight = data['avg_fight']
avg_weather = data['avg_weather']

total_games = wins + losses
norm_wins = wins / total_games
norm_losses = losses / total_games

# Bar chart of wins and losses for each team
plt.bar(teams, norm_wins, label='Wins')
plt.bar(teams, norm_losses, bottom=norm_wins, label='Losses')
# Add a subheading
plt.xlabel('Team')
plt.ylabel('Proportion of games won/lost')
plt.title('Team Wins and Losses', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Quick-Win Synergys - Higher is Better', y=0.95, fontsize=12)
plt.legend()
plt.show()

plt.hist(avg_fight, bins=16, edgecolor='black')
plt.xlabel('Average Length of Fight')
plt.ylabel('Frequency')
plt.title('Distribution of Average Length of Fight for a Single Team', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Quick-Win Synergys - Lower is Better', y=0.95, fontsize=12)
plt.show()

plt.hist(avg_weather, bins=16, edgecolor='black')
plt.xlabel('Average Number of Weather Changes per Battle')
plt.ylabel('Number of Teams')
plt.title('Distribution of Average Number of Weather Changes per Battle for Each Team', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Quick-Win Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()

plt.hist(data['avg_switch'], bins=5, edgecolor='black')
plt.xlabel('Average Number of Switches per Battle')
plt.ylabel('Frequency')
plt.title('Histogram of Average Number of Switches per Battle', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Quick-Win Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()


#--------------------------------------------------------------------------------------------------------------------
# Switch-Ins

# Load the text file and skip the first row
data = np.loadtxt('Outputs/Switch_Ins_outputMatrix.txt', dtype=dtypes, skiprows=1)

# Extract the data
teams = data['team']
wins = data['wins']
losses = data['losses']
avg_switch = data['avg_switch']
avg_ko = data['avg_ko']
avg_fight = data['avg_fight']
avg_weather = data['avg_weather']

total_games = wins + losses
norm_wins = wins / total_games
norm_losses = losses / total_games

# Bar chart of wins and losses for each team
plt.bar(teams, norm_wins, label='Wins')
plt.bar(teams, norm_losses, bottom=norm_wins, label='Losses')
# Add a subheading
plt.xlabel('Team')
plt.ylabel('Proportion of games won/lost')
plt.title('Team Wins and Losses', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Switch-In Synergys - Higher is Better', y=0.95, fontsize=12)
plt.legend()
plt.show()

plt.hist(avg_fight, bins=16, edgecolor='black')
plt.xlabel('Average Length of Fight')
plt.ylabel('Frequency')
plt.title('Distribution of Average Length of Fight for a Single Team', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Switch-In Synergys - Lower is Better', y=0.95, fontsize=12)
plt.show()

plt.hist(avg_weather, bins=16, edgecolor='black')
plt.xlabel('Average Number of Weather Changes per Battle')
plt.ylabel('Number of Teams')
plt.title('Distribution of Average Number of Weather Changes per Battle for Each Team', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Switch-In Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()

plt.hist(data['avg_switch'], bins=5, edgecolor='black')
plt.xlabel('Average Number of Switches per Battle')
plt.ylabel('Frequency')
plt.title('Histogram of Average Number of Switches per Battle', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Switch-In Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()

#--------------------------------------------------------------------------------------------------------------------
# Weather

# Load the text file and skip the first row
data = np.loadtxt('Outputs/Weather_outputMatrix.txt', dtype=dtypes, skiprows=1)

# Extract the data
teams = data['team']
wins = data['wins']
losses = data['losses']
avg_switch = data['avg_switch']
avg_ko = data['avg_ko']
avg_fight = data['avg_fight']
avg_weather = data['avg_weather']

total_games = wins + losses
norm_wins = wins / total_games
norm_losses = losses / total_games

# Bar chart of wins and losses for each team
plt.bar(teams, norm_wins, label='Wins')
plt.bar(teams, norm_losses, bottom=norm_wins, label='Losses')
# Add a subheading
plt.xlabel('Team')
plt.ylabel('Proportion of games won/lost')
plt.title('Team Wins and Losses', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Weather Synergys - Higher is Better', y=0.95, fontsize=12)
plt.legend()
plt.show()

plt.hist(avg_fight, bins=16, edgecolor='black')
plt.xlabel('Average Length of Fight')
plt.ylabel('Frequency')
plt.title('Distribution of Average Length of Fight for a Single Team', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Weather Synergys - Lower is Better', y=0.95, fontsize=12)
plt.show()

plt.hist(avg_weather, bins=16, edgecolor='black')
plt.xlabel('Average Number of Weather Changes per Battle')
plt.ylabel('Number of Teams')
plt.title('Distribution of Average Number of Weather Changes per Battle for Each Team', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Weather Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()

plt.hist(data['avg_switch'], bins=5, edgecolor='black')
plt.xlabel('Average Number of Switches per Battle')
plt.ylabel('Frequency')
plt.title('Histogram of Average Number of Switches per Battle', y=1.1, fontsize=16, fontweight='bold')
plt.suptitle('Weather Synergys - Higher is Better', y=0.95, fontsize=12)
plt.show()
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 23:53:03 2023

@author: craig
"""

import numpy as np
import json

# Open the file for reading
with open("Outputs/Win_Loss_Synergys_outputMatrix.txt", "r") as infile:
    # Skip the first line (the header)
    infile.readline()
    # Load the matrix using np.loadtxt()
    team = np.loadtxt(infile, dtype=int)
    
with open('Uber_Main_JSON_Files/Uber_Main_teamNumbers_Win_Loss_Synergy.json', 'r') as infile:
    teamNumbers = json.load(infile)
    
# =============================================================================
# Parse output and store data in a series of np arrays/dics
#
# Data structure:
#   Team Matrix:
#       Team number
#       Team Wins
#       Team Losses
#       average number of switch outs/switch ins
#       average number of pokemon KOd on the winning team (how close the match was)
#       average length of a fight for a single team
#       average number of weather changes per battle
#       number of battles fought (for average calculation purposes)
#       Win/Loss Ratio
#   Pokemon Matrix:
#       Pokemon Number
#       Individual Pokemon KOs
#       Wins for a team containing the pokemon
#       appearence of pokemon on top 1000 teams
#   Ability Matrix:
#       Ability name
#       number of times used on top 1000 teams
#   Item Matrix:
#       Item Name
#       number of times used on top 1000 teams
# =============================================================================

ratios = team[:,1] / team[:,2]
team_with_ratios = np.hstack((team, ratios[:,np.newaxis]))
# Get the indices that would sort the first column in descending order
sort_indices = np.argsort(team_with_ratios[:,8])[::-1]

# Sort the matrix based on the first column
team_sorted = team_with_ratios[sort_indices]

print("Top 10 Teams:")
[print(teamNumbers.get(str(int(i))), int(i)) for i in team_sorted[:10,0].tolist()]

print("\nBottom 10 Teams:")
[print(teamNumbers.get(str(int(i))), int(i)) for i in team_sorted[::-1][:10,0].tolist()]

print("\n")
print(team_sorted[:10,8].tolist())
print(team_sorted[::-1][:10,8].tolist())
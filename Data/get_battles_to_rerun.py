import itertools
import json
import statistics
import subprocess
import multiprocessing
import threading
import time
from timeit import default_timer as timer
import numpy as np
from tqdm import tqdm

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
#       Synergy Rating!
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
filename = "Inputs/Uber_Main.txt"
teamNumbers = {}

with open('Uber_Main_JSON_Files/Weather/' + filename[7:-4] + '_Weather_teamNumbers.json', 'r') as infile:
    teamNumbers = json.load(infile)
noOfTeams = len(teamNumbers)


pokemonCounter = 1
battleCounter = 0
#with open("Outputs/Switch_Ins_Outputs/Switch_Ins_Output.txt") as o:
with open("Outputs\Weather_Outputs\combined_output.txt") as o:
    lines = o.readlines() # read output file
    
    # get number of total pokemon for building pokemon matrix
    with open (filename) as g:
        mons = g.readlines()
        for line in mons:
            if line.startswith("|"):
                pokemonCounter += 1
    
    # build team matrix and pokemon matrix
    team = np.zeros((noOfTeams, 8))
    for i in range(noOfTeams):
        team[i][0] = i

    pokemon = np.zeros((pokemonCounter, 6))
    
    battles_to_rerun = []
    
    switchIns_team1 = 0
    switchIns_team2 = 0
    KOs_team1 = 0
    KOs_team2 = 0
    turns = 0
    weatherChanges = 0
    error=0
    # Main loop for parser
    for n, line in tqdm(enumerate(lines)):
        if line.startswith("TypeError"):
            error = 1
        if line.startswith("(node:"):
            error = 1
        if line.startswith("C:\Individual_Project"):
            error = 1
        if line.startswith("Error"):
            error = 1
        if line.startswith("[[[[["):
            battleStart = n
            team1 = int(lines[battleStart+1].split(" ")[0])
            team2 = int(lines[battleStart+1].split(" ")[2])
        if line.startswith("]]]]]"):
            try:
                team1
            except NameError:
                error=1
            try:
                team2
            except NameError:
                error=1
            if error == 0:
                pass
            if error != 0:
                battles_to_rerun.append([teamNumbers[str(team1)], teamNumbers[str(team2)]])
                error = 0

print(len(battles_to_rerun))
with open(filename[7:-4] + '_Weather_rerun_battles.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(battles_to_rerun, outfile)
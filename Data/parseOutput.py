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

with open('Uber_Main_JSON_Files/Weather/Uber_Main_Weather_teamNumbers.json', 'r') as infile:
    teamNumbers = json.load(infile)
noOfTeams = len(teamNumbers)


pokemonCounter = 1
battleCounter = 0
with open("Outputs/Weather_Final_Output.txt") as o:
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
            error=1
        if line.startswith("(node:"):
            error=1
        if line.startswith("C:\Individual_Project"):
            error = 1
        if line.startswith("Error"):
            error = 1
        if line.startswith("[[[[["):
            if lines[n+1].startswith("[[[[["):
                pass
            else:
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
                battleEnd = n
                # get winning team
                if lines[battleEnd-1].startswith("|win|Bot 1"):
                    winner, loser = 1, 2
                elif lines[battleEnd-1].startswith("|win|Bot 2"):
                    winner, loser = 2, 1
                else:
                    winner, loser = 0, 0
                
                #update team matrix
                if winner == 1:
                    team[team1][1] = team[team1][1] + 1
                    team[team1][4] = team[team1][4] + KOs_team2 # to be divided by number of wins [2]
                    team[team2][2] = team[team2][2] + 1
                if winner == 2:
                    team[team2][1] = team[team2][1] + 1
                    team[team2][4] = team[team2][4] + KOs_team1
                    team[team1][2] = team[team1][2] + 1
                team[team1][3] = team[team1][3] + switchIns_team1 # to be divided by number of battles [7]
                team[team2][3] = team[team2][3] + switchIns_team2
                team[team1][5] = team[team1][5] + turns
                team[team2][5] = team[team2][5] + turns
                team[team1][6] = team[team1][6] + weatherChanges # to be divided by number of battles [7]
                team[team2][6] = team[team2][6] + weatherChanges
                team[team1][7] = team[team1][7] + 1
                team[team2][7] = team[team2][7] + 1

            switchIns_team1 = 0
            switchIns_team2 = 0
            KOs_team1 = 0
            KOs_team2 = 0
            turns = 0
            weatherChanges = 0
            if error != 0:
                error = 0

        if line.startswith("|turn"):
            turns += 1
        if line.startswith("|switch|p1a"):
            switchIns_team1 += 1
        if line.startswith("|switch|p2a"):
            switchIns_team2 += 1
        if line.startswith("|faint|p2a:"):
            KOs_team1 += 1
        if line.startswith("|faint|p1a:"):
            KOs_team2 += 1
        if line.startswith("|-weather"):
            weatherChanges += 1
    team[:, 3] = np.nan_to_num(team[:, 3] / team[:, 7], 0)
    team[:, 4] = np.nan_to_num(team[:, 4] / team[:, 1], 0)
    team[:, 5] = np.nan_to_num(team[:, 5] / team[:, 7], 0)
    team[:, 6] = np.nan_to_num(team[:, 6] / team[:, 7], 0)
    synergyRatings_win_loss = dict(zip([i for i in range(noOfTeams)], np.nan_to_num(team[:, 1] / team[:, 2], 0))) #currently going by win loss ratios, but might refine later
    synergyRatings_quick_wins = dict(zip([i for i in range(noOfTeams)], np.nan_to_num((50*(team[:, 1] / team[:, 2]) - 30*team[:, 5] - 20*team[:, 4]) / 50 + 30 + 20, 0)))
    synergyRatings_switch_ins = dict(zip([i for i in range(noOfTeams)], np.nan_to_num((50*(team[:, 1] / team[:, 2]) - 20*team[:, 3] - 20*team[:, 4]) / 50 + 20 + 20, 0)))
    synergyRatings_weather = dict(zip([i for i in range(noOfTeams)], np.nan_to_num((50*(team[:, 1] / team[:, 2]) - 30*team[:, 6] - 20*team[:, 4]) / 50 + 30 + 20, 0)))
    team = np.around(team)
    np.set_printoptions(threshold=10)
    #print(team)
    with open("Outputs/Weather_outputMatrix.txt", "a") as outfile:
        outfile.truncate(0)
        outfile.write("Team Matrix\n")
        np.savetxt(outfile, team, fmt='%.10d')
        outfile.write("\n\n")

#To Delete
#with open("./Uber_Main_Teams_Of_2_Synergys-Win-Loss.txt", "a") as outfile:
#    outfile.truncate(0)
#    outfile.write(json.dumps(synergyRatings_win_loss))
#with open("./Uber_Main_Teams_Of_2_Synergys-Quick-Win.txt", "a") as outfile:
#    outfile.truncate(0)
#    outfile.write(json.dumps(synergyRatings_quick_wins))
#    
#with open("./Uber_Main_Teams_Of_2_Synergys-Switch-Ins.txt", "a") as outfile:
#    outfile.truncate(0)
#    outfile.write(json.dumps(synergyRatings_switch_ins))
#    
#with open("./Uber_Main_Teams_Of_2_Synergys-Weather.txt", "a") as outfile:
#    outfile.truncate(0)
#    outfile.write(json.dumps(synergyRatings_weather))
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:04:58 2022

@author: craig
"""
import itertools
import json
import statistics
import subprocess
import multiprocessing
import threading
import time
import numpy as np
from timeit import default_timer as timer

#Counts all pokemon builds in the list
def count(filename):
    counter = 0
    with open (filename) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("|"):
                counter += 1
    return counter

#Counts all pokemon not including duplicates
def countNoDuplicates(filename):
    counter = 0
    dex = []
    with open (filename) as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("|"):
                mon = line[1:].split()[0]
                if not mon in dex:
                    dex.append(mon)
                    counter += 1
    return counter

# =============================================================================
# Gets all possible combination of 6 pokemon from a passed in txt file
# Input should be in pokemon showdown format seperated with a "|" character at the start of each new pokemon
# =============================================================================
def getTeamCombinations(filename):
    dex = []
    teamNumbers = {}
    with open (filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("|"):
                dex.append((line[1:].split('@')[0].strip(), i))
                
    all_combinations = list(itertools.combinations(dex, 6))
    
    teams = []
    for team in all_combinations:
        if len(team) == 6 and team not in teams and len(set([i[0] for i in team])) == 6:
                teams.append(list(team))
    #print(teams)
    #print(len(teams))

    #build a dictionary of teams mapped to team numbers
    for i, t in enumerate(teams):
        teamNumbers[i] = t
    
    team_matchups = list(itertools.combinations(teams, 2))
    #print(team_matchups)
    #print(len(team_matchups))
    
    return team_matchups, teamNumbers

def getTeamCombinations_synergy(filename, synergyRatings, teamNumbers):
    dex = []
    with open (filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("|"):
                dex.append((line[1:].split('@')[0].strip(), i))
                
    all_combinations = list(itertools.combinations(dex, 6))
    
    teams = []
    temp = 0
    for team in all_combinations:
        if len(team) == 6 and team not in teams and len(set([i[0] for i in team])) == 6:
            #print(team)
            team_pairs = list(itertools.combinations(team, 2))
            for pair in team_pairs:
                if len(pair) == 2:
                    if synergyRatings.get(get_keys_from_value(teamNumbers, list(pair))[0]) >= 0.6:
                        pass
                    else:
                        temp = 1
            if temp == 0:
                teams.append(list(team))
            else:
                temp = 0
    #print(teams)
    #print(len(teams))

    team_matchups = list(itertools.combinations(teams, 2))
    return team_matchups
# =============================================================================
# Gets all possible combinations of 2v2 matchups from a passed in txt file
# Input should be in pokemon showdown format seperated with a "|" character at the start of each new pokemon
# =============================================================================
def getTeamsOfTwo(filename):
    dex = []
    teamNumbers = {}
    with open (filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("|"):
                dex.append((line[1:].split('@')[0].strip(), i))
                
    all_combinations = list(itertools.combinations(dex, 2))
    
    teams = []
    for team in all_combinations:
        if len(team) == 2 and team not in teams and len(set([i[0] for i in team])) == 2:
                teams.append(list(team))
    #print(teams)
    #print(len(teams))

    #build a dictionary of teams mapped to team numbers
    for i, t in enumerate(teams):
        teamNumbers[i] = t
    
    team_matchups = list(itertools.combinations(teams, 2))
    #print(team_matchups)
    #print(len(team_matchups))
    
    return team_matchups, teamNumbers

# =============================================================================
# Runs a single simulation for some matchup passed in
# =============================================================================
def runSimulation(matchup, threadNo, filename, teamNumbers):
    # get number of each team from the teamNumbers dict
    team1No = get_keys_from_value( teamNumbers, matchup[0])[0]
    team2No = get_keys_from_value( teamNumbers, matchup[1])[0]

    if len(matchup[0]) == 2 and len(matchup[1]) == 2:
        game = "2v2"
    if len(matchup[0]) == 6 and len(matchup[1]) == 6:
        game = "6v6"
    
    with open (filename) as f:
        lines = f.readlines()
        with open ("./WorkerFiles/" + threadNo + "1.txt", "a") as g: 
            g.truncate(0)
            for i in matchup[0]:
                for j in range(8):
                    g.write(lines[i[1]+j].replace("|", ""))
                g.write("\n")
            with open ("./WorkerFiles/" + threadNo + "2.txt", "a") as h: 
                h.truncate(0)
                for i in matchup[1]:
                    for j in range(8):
                        h.write(lines[i[1]+j].replace("|", ""))
                    h.write("\n")
        while True:
            #mycommand = "cd ../pokemon-showdown && node build && node .sim-dist/examples/battle-stream-example " + threadNo + " " + str(team1No) + " " + str(team2No)
            mycommand = "cd ../pokemon-showdown && node dist/sim/examples/simulation-test-1 " + threadNo + " " + str(team1No) + " " + str(team2No)
            result = subprocess.getoutput(mycommand)
            # if the battle fails we retry, sometimes showdown fails for some unexpected reason
            if not (result.startswith("C:\Individual_Project") or result.startswith("node:internal") or result.startswith("TypeError")):
                try:
                    if not (result[:40].split("\n")[2].startswith("TypeError") or result[:40].split("\n")[2].startswith("C:\Individual_Project")):
                        break
                except:
                    break
        with open ("./WorkerOutputs/" + threadNo + ".txt", "a") as o: 
            o.write(result + "\n]]]]]\n")
        return(result)

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

with open ("./output.txt", "a") as o: 
    o.truncate(0)
#print(count("Uber_top_10.txt"))
#print(countNoDuplicates("Uber_top_10.txt"))

filename = "Inputs/Uber.txt"
teams, teamNumbers = getTeamsOfTwo(filename)
#teams, teamNumbers = getTeamCombinations(filename)

print(len(teams))
n = 1000 #number of battles to simulate
teams = teams[:n] #comment this out to simulate all battles
noOfTeams = len(teamNumbers)
noOfThreads = 50

subprocess.getoutput("cd ../pokemon-showdown && node build")
threads = []
start = time.time()

while len(teams) >= noOfThreads:
    for i in range(noOfThreads):
        thread = threading.Thread(
            target=runSimulation, args=(teams[0], str(i+1), filename, teamNumbers))
        threads.append(thread)
        teams.pop(0)
    
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    threads.clear()
    print(len(teams)) #for keeping track of where we are

#speed up leftover battles
while len(teams) >= 25:
    for i in range(25):
        thread = threading.Thread(
            target=runSimulation, args=(teams[0], str(i+1), filename, teamNumbers))
        threads.append(thread)
        teams.pop(0)
    
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    threads.clear()
    print(len(teams)) #for keeping track of where we are

#speed up leftover battles
while len(teams) >= 10:
    for i in range(10):
        thread = threading.Thread(
            target=runSimulation, args=(teams[0], str(i+1), filename, teamNumbers))
        threads.append(thread)
        teams.pop(0)
    
    for i in threads:
        i.start()
    for i in threads:
        i.join()
    threads.clear()
    print(len(teams)) #for keeping track of where we are

for i in teams:
    runSimulation(i, "0", filename, teamNumbers)

infiles = [str(i+1) for i in range(noOfThreads)]
with open("output.txt", "a") as outfile:
    for i in infiles:
        with open("./WorkerOutputs/" + i + ".txt", "r") as output:
            for i in output.readlines():
                outfile.write(i)

infiles.append("0")
for i in infiles:
    with open("./WorkerOutputs/" + i + ".txt", "w") as output:
        output.truncate(0)
            

end = time.time()
print("ran in " + str(end-start) + " Seconds Overall")
print(str((end - start)/n) + " Seconds Per Sim On Average")

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

pokemonCounter = 1
battleCounter = 0
with open("output.txt") as o:
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
    for n, line in enumerate(lines):
        if line.startswith("TypeError"):
            error=1
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
    synergyRatings = dict(zip([i for i in range(noOfTeams)], np.nan_to_num(team[:, 1] / team[:, 2], 0))) #currently going by win loss ratios, but might refine later
    team = np.around(team)
    np.set_printoptions(threshold=10)
    #print(team)
    with open("./outputMatrix.txt", "a") as outfile:
        outfile.truncate(0)
        outfile.write("Team Matrix\n")
        np.savetxt(outfile, team, fmt='%.10d')
        outfile.write("\n\n")

#To Delete
with open("./synergys.txt", "a") as outfile:
    outfile.truncate(0)
    outfile.write("Synergy Ratings\n")
    outfile.write(json.dumps(synergyRatings))
    outfile.write("\n\n")

#finalMatchups = getTeamCombinations_synergy(filename, synergyRatings, teamNumbers)
#print(len(finalMatchups))
            

        
            


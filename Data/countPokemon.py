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
from timeit import default_timer as timer
import numpy as np

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

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

#print(count("Uber_top_10.txt"))
#print(countNoDuplicates("Uber_top_10.txt"))

filename = "Inputs/Uber_Main.txt"
teams, teamNumbers = getTeamsOfTwo(filename)
#teams, teamNumbers = getTeamCombinations(filename)
print(len(teams))

with open(filename[7:-4] + '_battles.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(teams, outfile)

with open(filename[7:-4] + '_teamNumbers.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(teamNumbers, outfile, indent=4)
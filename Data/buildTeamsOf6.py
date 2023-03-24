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
from tqdm import tqdm
import concurrent.futures

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
# Get all possible teams of 6, and return a set of battles for them
    # note this version should only be run when the inputs size is very small
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

    #build a dictionary of teams mapped to team numbers
    for i, t in enumerate(teams):
        teamNumbers[i] = t
    
    team_matchups = list(itertools.combinations(teams, 2))
    
    return team_matchups, teamNumbers

# =============================================================================
# Gets all possible combination of 6 pokemon from a passed in txt file, and constructs teams using synergy ratings
# Input should be in pokemon showdown format seperated with a "|" character at the start of each new pokemon
# =============================================================================
def getTeamCombinations_synergy(filename, synergyRatings, teamNumbers):
    # build dex from input file
    dex = []
    with open (filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("|"):
                dex.append(((line[1:].split('@')[0].strip(), i), (line[1:].split('@ ')[1].strip())))
    
    # get all combinations that don't violate Showdown clauses
    all_combinations = (element for element in itertools.combinations(dex, 6)
                        if len(set([inner_list[0][0] for inner_list in element])) == 6
                        and len(set([inner_list[1] for inner_list in element])) == 6)
    
    #free some memory
    del lines
    del dex
    
    # define synergy threshold
    SYNERGY_THRESHOLD = sorted(synergyRatings.values(), reverse=True)[470]
    
    # remove teams that have pairs with bad synergy
    teams = []
    for team in tqdm(all_combinations):
        temp = 0
        team_pairs = itertools.combinations(team, 2)
        for pair in team_pairs:
            pair = tuple([pair[0][0], pair[1][0]])
            if len(pair) == 2:
                if synergyRatings.get(teamNumbers.get(pair)) >= SYNERGY_THRESHOLD:
                    pass
                else:
                    temp = 1
        if temp == 0:
            teams.append([i[0] for i in team])
    
    print(len(teams))
    del all_combinations
    teamNumbers = {}
    for i, t in enumerate(teams):
        teamNumbers[i] = t
    team_matchups = list(itertools.combinations(teams, 2))
    return team_matchups, teamNumbers

# =============================================================================
# Gets all possible combinations of 2v2 matchups from a passed in txt file
# Input should be in pokemon showdown format seperated with a "|" character at the start of each new pokemon
# =============================================================================
def getTeamsOfTwo(filename):
    # build dex from input file
    dex = []
    teamNumbers = {}
    with open (filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("|"):
                dex.append((line[1:].split('@')[0].strip(), i))

    # get all combinations that don't violate Showdown clauses
    all_combinations = list(itertools.combinations(dex, 2))
    teams = []
    for team in all_combinations:
        if len(team) == 2 and team not in teams and len(set([i[0] for i in team])) == 2:
                teams.append(list(team))

    #build a dictionary of teams mapped to team numbers
    for i, t in enumerate(teams):
        teamNumbers[i] = t
    
    print(len(teams))
    team_matchups = list(itertools.combinations(teams, 2))
    return team_matchups, teamNumbers

# helper function which looks up a list of keys for a value
def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

# helper function which converts a list to a tuple
def list_to_tuple(list_of_lists):
    return tuple(tuple(inner_list) for inner_list in list_of_lists)

# load input files
filename = "Inputs/Uber_Main.txt"
with open('Uber_Main_JSON_Files/teams_of_2/' + filename[7:-4] + '_Teams-Of-2_teamNumbers.json', 'r') as infile:
    teamNumbers = json.load(infile)
with open('Uber_Main_Teams_Of_2_Synergys-Weather.txt', 'r') as infile:
    synergyRatings = json.loads(infile.read())
teamNumbers = {list_to_tuple(v): k for k, v in teamNumbers.items()}

# build teams
teams, teamNumbers = getTeamCombinations_synergy(filename, synergyRatings, teamNumbers)
print(len(teams))

# write teams
with open(filename[7:-4] + '_Weather_battles.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(teams, outfile)

with open(filename[7:-4] + '_Weather_teamNumbers.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(teamNumbers, outfile, indent=4)
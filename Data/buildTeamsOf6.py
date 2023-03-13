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

# =============================================================================
# Gets all possible combination of 6 pokemon from a passed in txt file
# Input should be in pokemon showdown format seperated with a "|" character at the start of each new pokemon
# =============================================================================
def getTeamCombinations_synergy(filename, synergyRatings, teamNumbers):
    #meanSynergy = np.mean(list(synergyRatings.values()))
    dex = []
    with open (filename) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if line.startswith("|"):
                dex.append(((line[1:].split('@')[0].strip(), i), (line[1:].split('@ ')[1].strip())))
                
    #all_combinations = list(itertools.combinations(dex, 6))
    #all_combinations = [element for element in all_combinations 
    #                    if len(set([inner_list[0][0] for inner_list in element])) == 6
    #                    # make sure for each team, no 2 pokemon have the same item
    #                    and len(set([inner_list[1] for inner_list in element])) == 6
    #                    ]
    all_combinations = (element for element in itertools.combinations(dex, 6)
                        if len(set([inner_list[0][0] for inner_list in element])) == 6
                        and len(set([inner_list[1] for inner_list in element])) == 6)
    #all_combinations = [[(pokemon[0], pokemon[1]) for pokemon in team] for team in all_combinations]
    
    #free some memory
    del lines
    del dex
    
    SYNERGY_THRESHOLD = sorted(synergyRatings.values(), reverse=True)[574]
    
    teams = []
    for team in tqdm(all_combinations):
        temp = 0
        team_pairs = itertools.combinations(team, 2)
        #team_pairs = [[list(t) for t in inner_list] for inner_list in team_pairs]
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
    
    print(len(teams))
    team_matchups = list(itertools.combinations(teams, 2))
    #print(team_matchups)
    #print(len(team_matchups))
    
    return team_matchups, teamNumbers

def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

def list_to_tuple(list_of_lists):
    return tuple(tuple(inner_list) for inner_list in list_of_lists)

filename = "Inputs/Uber_Main.txt"
with open('Uber_Main_JSON_Files/teams_of_2/' + filename[7:-4] + '_teamNumbers_TeamsOf2.json', 'r') as infile:
    teamNumbers = json.load(infile)
with open('Uber_Main_Teams_Of_2_Synergys-Switch-Ins.txt', 'r') as infile:
    synergyRatings = json.loads(infile.read())
teamNumbers = {list_to_tuple(v): k for k, v in teamNumbers.items()}

teams, teamNumbers = getTeamCombinations_synergy(filename, synergyRatings, teamNumbers)
print(len(teams))

with open(filename[7:-4] + '_Switch-Ins_battles.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(teams, outfile)

with open(filename[7:-4] + '_Switch-Ins_teamNumbers.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(teamNumbers, outfile, indent=4)
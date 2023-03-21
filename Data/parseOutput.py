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
import re

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
#       average number of weather changes to sandstorm
#       average number of weather changes to hail
#       average number of weather changes to sun
#       average number of weather changes to rain
#       number of battles fought (for average calculation purposes)
#   Pokemon Matrix:
#       Pokemon Number
#       Individual Pokemon KOs
#       Wins for the top performing team containing the pokemon
#       appearence of pokemon on top 100 teams
#   Ability Dict:
#       Ability name
#       number of times used on top 100 teams
#   Item Dict:
#       Item Name
#       number of times used on top 100 teams
#   Move Dict:
#       Move Name
#       KOs
# =============================================================================
filename = "Inputs/Uber_Main.txt"
model = "Weather"

with open(filename[7:-4] + '_JSON_Files/' + model + '/' + filename[7:-4] + '_' + model.replace("_", "-") + '_teamNumbers.json', 'r') as infile:
    teamNumbers = json.load(infile)
noOfTeams = len(teamNumbers)

dex = []
with open ("Inputs/" + filename[7:-4] + ".txt") as f:
    lines = f.readlines()
    all_mons = list(itertools.chain.from_iterable(teamNumbers.values()))
    for i, line in enumerate(lines):
        if line.startswith("|"):
            dex.append((line[1:].split('@')[0].strip(), i, line[1:].split('@')[1].strip(), lines[i+1][9:].strip()))
# maps pokemon line number to the species, item and ability
dex = {i[1]:(i[0], i[2], i[3]) for i in dex if [i[0], i[1]] in all_mons}
# maps pokemon line numbers to its row in the pokemon matrix
dexNumbers = {i:n for n, i in enumerate(dex.keys())}

pokemonCounter = len(dex)
battleCounter = 0
with open('Outputs/' + model + '_Final_Output.txt') as o:
    lines = o.readlines() # read output file
    
    # build team matrix
    team = np.zeros((noOfTeams, 11))
    for i in range(noOfTeams):
        team[i][0] = i

    # build pokemon matrix
    pokemon = np.zeros((pokemonCounter, 4))
    for i in range(pokemonCounter):
        pokemon[i][0] = i
        
    # build item, ability and move dict
    item = {}
    ability = {}
    move = {}
    
    switchIns_team1 = 0
    switchIns_team2 = 0
    KOs_team1 = 0
    KOs_team2 = 0
    turns = 0
    weatherChangesSand = 0
    weatherChangesRain = 0
    weatherChangesSun = 0
    weatherChangesHail = 0
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
                team[team1][3] = team[team1][3] + switchIns_team1 # to be divided by number of battles [10]
                team[team2][3] = team[team2][3] + switchIns_team2
                team[team1][5] = team[team1][5] + turns
                team[team2][5] = team[team2][5] + turns
                team[team1][6] = team[team1][6] + weatherChangesSand # to be divided by number of battles [10]
                team[team2][6] = team[team2][6] + weatherChangesSand
                team[team1][7] = team[team1][7] + weatherChangesHail # to be divided by number of battles [10]
                team[team2][7] = team[team2][7] + weatherChangesHail
                team[team1][8] = team[team1][8] + weatherChangesSun # to be divided by number of battles [10]
                team[team2][8] = team[team2][8] + weatherChangesSun
                team[team1][9] = team[team1][9] + weatherChangesRain # to be divided by number of battles [10]
                team[team2][9] = team[team2][9] + weatherChangesRain
                team[team1][10] = team[team1][10] + 1
                team[team2][10] = team[team2][10] + 1

            switchIns_team1 = 0
            switchIns_team2 = 0
            KOs_team1 = 0
            KOs_team2 = 0
            turns = 0
            weatherChangesSand = 0
            weatherChangesHail = 0
            weatherChangesSun = 0
            weatherChangesRain = 0
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
            ln = n
            for i in range(10):
                ln -= 1
                if lines[ln].startswith("|move|p1a"):
                    pokemon_ko = lines[ln].split('|')[2][5:].strip()
                    move_ko = re.split(r"[|]", lines[ln])[3].strip()
                    if move_ko not in move:
                        move[move_ko] = 1
                    else:
                        move[move_ko] += 1
                    if len([sublist[1] for sublist in teamNumbers.get(str(team1)) if sublist[0].startswith(pokemon_ko)]) != 0:
                        pm_linenumber = [sublist[1] for sublist in teamNumbers.get(str(team1)) if sublist[0].startswith(pokemon_ko)][0]
                        pokemonNo = dexNumbers.get(pm_linenumber)
                        pokemon[pokemonNo][1] = pokemon[pokemonNo][1] + 1
                        break;
        if line.startswith("|faint|p1a:"):
            KOs_team2 += 1
            ln = n
            for i in range(10):
                ln -= 1
                if lines[ln].startswith("|move|p2a"):
                    pokemon_ko = lines[ln].split('|')[2][5:].strip()
                    move_ko = re.split(r"[|]", lines[ln])[3].strip()
                    if move_ko not in move:
                        move[move_ko] = 1
                    else:
                        move[move_ko] += 1
                    if len([sublist[1] for sublist in teamNumbers.get(str(team2)) if sublist[0].startswith(pokemon_ko)]) != 0:
                        pm_linenumber = [sublist[1] for sublist in teamNumbers.get(str(team2)) if sublist[0].startswith(pokemon_ko)][0]
                        pokemonNo = dexNumbers.get(pm_linenumber)
                        pokemon[pokemonNo][1] = pokemon[pokemonNo][1] + 1
                        break;
        if line.startswith("|-weather|Sandstorm"):
            weatherChangesSand += 1
        if line.startswith("|-weather|Hail"):
            weatherChangesHail += 1
        if line.startswith("|-weather|RainDance"):
            weatherChangesRain += 1
        if line.startswith("|-weather|SunnyDay"):
            weatherChangesSun += 1
        
    team[:, 3] = np.nan_to_num(team[:, 3] / team[:, 10], 0)
    team[:, 4] = np.nan_to_num(team[:, 4] / team[:, 1], 0)
    team[:, 5] = np.nan_to_num(team[:, 5] / team[:, 10], 0)
    team[:, 6] = np.nan_to_num(team[:, 6] / team[:, 10], 0)
    team[:, 7] = np.nan_to_num(team[:, 7] / team[:, 10], 0)
    team[:, 8] = np.nan_to_num(team[:, 8] / team[:, 10], 0)
    team[:, 9] = np.nan_to_num(team[:, 9] / team[:, 10], 0)
    synergyRatings_win_loss = dict(zip([i for i in range(noOfTeams)], np.nan_to_num(team[:, 1] / team[:, 2], 0))) #currently going by win loss ratios, but might refine later
    synergyRatings_quick_wins = dict(zip([i for i in range(noOfTeams)], np.nan_to_num((50*(team[:, 1] / team[:, 2]) - 30*team[:, 5] - 20*team[:, 4]) / 50 + 30 + 20, 0)))
    synergyRatings_switch_ins = dict(zip([i for i in range(noOfTeams)], np.nan_to_num((50*(team[:, 1] / team[:, 2]) - 20*team[:, 3] - 20*team[:, 4]) / 50 + 20 + 20, 0)))
    synergyRatings_weather = dict(zip([i for i in range(noOfTeams)], np.nan_to_num((50*(team[:, 1] / team[:, 2]) + 30*team[:, 6] - 20*team[:, 4]) / 50 + 30 + 20, 0)))
    team = np.around(team)
    np.set_printoptions(threshold=10, suppress=True)
    #print(team)
    with open('Outputs/' + model + '_outputMatrix.txt', "a") as outfile:
        outfile.truncate(0)
        outfile.write("Team Matrix\n")
        np.savetxt(outfile, team, fmt='%.10d')
        outfile.write("\n\n")
        
    ratios = team[:, 1] / team[:, 0]
    sorted_indices = np.argsort(ratios)
    sorted_team = team[sorted_indices]
    pokemon_on_top_100_teams = list(itertools.chain.from_iterable(list(map(lambda x: teamNumbers[x], [str(int(i)) for i in sorted_team[:100, 0].tolist()]))))
    for linenumber, mon in dex.items():
        for top100 in pokemon_on_top_100_teams:
            if [mon[0], linenumber] == top100:
                pokemon[dexNumbers.get(linenumber)][3] = pokemon[dexNumbers.get(linenumber)][3] + 1
                if mon[1] not in item:
                    item[mon[1]] = 1
                else:
                    item[mon[1]] += 1
                if mon[2] not in ability:
                    ability[mon[2]] = 1
                else:
                    ability[mon[2]] += 1
                    
    sorted_wins = [int(i) for i in sorted_team[:, 1].tolist()]
    sorted_teams = list(map(lambda x: teamNumbers[x], [str(int(i)) for i in sorted_team[:, 0].tolist()]))
    for linenumber, mon in dex.items():
        for n, team in enumerate(sorted_teams):
            if [mon[0], linenumber] in team:
                pokemon[dexNumbers.get(linenumber)][2] = sorted_wins[n]
    
    with open('Outputs/' + model + '_pokemonMatrix.txt', "a") as outfile:
        outfile.truncate(0)
        outfile.write("Pokemon Matrix\n")
        np.savetxt(outfile, pokemon, fmt='%.10d')
        outfile.write("\n\n")
    
    with open('Outputs/' + model + '_moveDict.json', "w") as outfile:
        outfile.truncate(0)
        json.dump(move, outfile)
        
    with open('Outputs/' + model + '_itemDict.json', "w") as outfile:
        outfile.truncate(0)
        json.dump(item, outfile)
        
    with open('Outputs/' + model + '_abilityDict.json', "w") as outfile:
        outfile.truncate(0)
        json.dump(ability, outfile)
    
    pokemonNumbers = {dexNumbers[k]:[v[0], k] for k, v in dex.items()}
    with open('Outputs/' + model + '_pokemonNumbers.json', "w") as outfile:
        outfile.truncate(0)
        json.dump(pokemonNumbers, outfile)

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
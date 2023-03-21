import itertools
import json
import statistics
import subprocess
import multiprocessing
import threading
import time
from timeit import default_timer as timer
import numpy as np

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
            #mycommand = "cd ../pokemon-showdown && node build && node ./dist/sim/examples/battle-stream-example"
            mycommand = "cd ../pokemon-showdown && node ./dist/sim/examples/Simulation-test-1 " + threadNo + " " + str(team1No) + " " + str(team2No)
            result = subprocess.getoutput(mycommand)
            # if the battle fails we retry, sometimes showdown fails for some unexpected reason
            if not (result.startswith("node:internal") or result.startswith("TypeError") or result.startswith("runtime")):
                try:
                    if not (result[:40].split("\n")[2].startswith("TypeError")):
                        break
                except:
                    break
        with open ("./WorkerOutputs/" + threadNo + ".txt", "a") as o: 
            o.write(result + "\n]]]]]\n")
        return(result)
    
def get_keys_from_value(d, val):
    return [k for k, v in d.items() if v == val]

filename = "Inputs/" + "Uber_Main.txt"
noOfThreads = 50

#read in teams
with open('Uber_Main_JSON_Files/' + filename[7:-4] + '_Weather_rerun_battles.json', 'r') as infile:
    teams = json.load(infile)

with open('Uber_Main_JSON_Files/Weather/' + filename[7:-4] + '_Weather_teamNumbers.json', 'r') as infile:
    teamNumbers = json.load(infile)

print(len(teams))
n = 100 # number of battles to stop running after
#teams = teams[:n] # comment this out to simulate all battles

noOfTeams = len(teamNumbers)

with open ("./output.txt", "a") as o: 
    o.truncate(0)
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
infiles.append("0")
with open("output.txt", "a") as outfile:
    for i in infiles:
        with open("./WorkerOutputs/" + i + ".txt", "r") as output:
            for i in output.readlines():
                outfile.write(i)

for i in infiles:
    with open("./WorkerOutputs/" + i + ".txt", "w") as output:
        output.truncate(0)
            

end = time.time()
print("ran in " + str(end-start) + " Seconds Overall")
print(str((end - start)/n) + " Seconds Per Sim On Average")
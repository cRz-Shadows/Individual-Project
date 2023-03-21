# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 10:37:54 2023

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

def split_json_by_n(filename, n):
    with open("Uber_Main_JSON_Files/" + filename[7:-4] + '_Weather_battles.json', 'r') as infile:
        teams = json.load(infile)
    chunks = [teams[i:i + n] for i in range(0, len(teams), n)]
    for i, chunk in enumerate(chunks):
        with open("Uber_Main_JSON_Files/" + filename[7:-4] + '_Weather_battles' + str(i) + '.json', 'w') as outfile:
            outfile.truncate(0)
            json.dump(chunk, outfile)


split_json_by_n("Inputs/Uber_Main.txt", 350000)
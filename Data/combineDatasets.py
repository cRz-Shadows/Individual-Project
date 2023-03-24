# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 17:39:21 2023

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

# =============================================================================
# This file can be used to combine sets of battles into one file, which can be run in runSimulations.py
# =============================================================================

filename = "Inputs/" + "Uber_Main.txt"

with open(filename[7:-4] + '_battles6.json', 'r') as infile:
    teams1 = json.load(infile)
    
with open(filename[7:-4] + '_battles7.json', 'r') as infile:
    teams2 = json.load(infile)

with open(filename[7:-4] + '_battles_6_7.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(teams1+teams2, outfile)
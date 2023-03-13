# -*- coding: utf-8 -*-
"""
Created on Sun Jan 29 10:16:45 2023

@author: craig
"""

infiles = [str(i+1) for i in range(80)]
with open("Uber_Main_0_output.txt", "a") as outfile:
    for i in infiles:
        with open("./Uber_Main_battles0_worker_outputs/" + i + ".txt", "r") as output:
            for i in output.readlines():
                outfile.write(i)
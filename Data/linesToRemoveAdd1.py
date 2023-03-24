# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 18:38:03 2023

@author: craig
"""

# =============================================================================
# Helper file which adds 1 to the linenumbers of a JSON of lines to remove
    # this was created to fix an error, and shouldn't be required for use
# =============================================================================

import json
from tqdm import tqdm

with open('Uber_Main_lines_To_Remove.json', 'r') as infile:
    lines_To_Remove = json.load(infile)
    
result = []
for sub_lst in tqdm(lines_To_Remove):
    result.append([x + 1 for x in sub_lst])
    
with open('Uber_Main_lines_To_Remove_add1.json', 'w') as outfile:
    outfile.truncate(0)
    json.dump(result, outfile)
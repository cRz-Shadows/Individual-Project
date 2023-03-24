# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 20:23:12 2023

@author: craig
"""

import os
from tqdm import tqdm

# =============================================================================
# This file can be used to combine output files, so that battles that have been 
# split up can have their whole output analysed
# =============================================================================

def combine_txt_files(directory, output_file):
    file_list = [f for f in os.listdir(directory) if f.endswith('.txt')]
    print(file_list)
    with open(output_file, 'w') as outfile:
        outfile.truncate()
        for filename in tqdm(file_list, desc='Combining Files'):
            with open(os.path.join(directory, filename)) as infile:
                for line in infile:
                    if line.strip():
                        outfile.write(line)

# Usage:
combine_txt_files('C:\Individual_Project\Data\Outputs\Weather_Outputs\Combine', 'C:\Individual_Project\Data\Outputs\Weather_Outputs\Weather_Final_Output_With_Errors.txt')
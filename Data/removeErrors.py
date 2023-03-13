# -*- coding: utf-8 -*-
"""
Created on Sun Feb  5 18:45:42 2023

@author: craig
"""

import json
from tqdm import tqdm
    
def remove_lines(file_name, start_end_points):
    with open(file_name, "r") as input_file, open("Outputs/Weather_Final_Output.txt", "w") as output_file:
        line_number = 0
        for line in tqdm(input_file):
            left = 0
            right = len(start_end_points) - 1
            line_in_range = False
            while left <= right:
                mid = (left + right) // 2
                if start_end_points[mid][0] <= line_number < start_end_points[mid][1]:
                    line_in_range = True
                    break
                elif line_number >= start_end_points[mid][1]:
                    left = mid + 1
                else:
                    right = mid - 1
            if not line_in_range:
                output_file.write(line)
            line_number += 1
    
with open('Uber_Main_lines_To_Remove.json', 'r') as infile:
    lines_To_Remove = json.load(infile)
    
remove_lines("Outputs/Weather_Outputs/Weather_Final_Output_With_Errors.txt", lines_To_Remove)
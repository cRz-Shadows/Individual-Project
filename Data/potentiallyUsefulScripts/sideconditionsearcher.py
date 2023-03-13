# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 18:58:56 2023

@author: craig
"""

def search_text_file(filepath):
  counter = 0
  # Open the text file
  with open(filepath, 'r') as file:
    # Read the file line by line
    for line in file:
      # Check if the line contains 'sideConditions: {' and isn't immediately followed by an '}' character
      if 'multihit: ' in line and not ('undefined' in line):
        # Initialize an empty string to store the occurrence
        occurrence = line
        # Read the next lines until we find the closing '}' character
        while True:
          line = file.readline()
          # Add the line to the occurrence
          occurrence += line
          # If the line contains the closing '}' character, stop reading
          if '}' in line:
            counter += 1
            if counter >= 0:
                break
        # Print the occurrence
        print(occurrence)
  return False

# Test the function with a sample text file
filepath = 'output.txt'
if search_text_file(filepath):
  print("Found an occurrence of the string 'sideConditions: {' that isn't immediately followed by an '}' character in the file.")
else:
  print("Did not find an occurrence of the string 'sideConditions: {' that isn't immediately followed by an '}' character in the file.")
# Class: Northwestern CS 349 Fall 2024
# ------------------------------------

# Professor: David Demeter
# ------------------------------------

# Contributers:
# ------------------------------------
#   Raymond Gu
#   Mimi Zhang
#   Alvin Xu
#   Rhema Phiri
#   Eshan Haq

import csv

# Parse Function
# --------------------------------------------------------------------------------------------
def parse(filename):
  '''
  Purpose: Returns attribute information and all the data in array of dictionaries.

  Output:
  - Out: A list of examples with each example being a dictionary that maps attribute to the
         value of that attribute for that example.
  '''
  # Initialize variables
  out = []

  # Read the file
  csvfile = open(filename,'r')
  fileToRead = csv.reader(csvfile)
  headers = next(fileToRead)

  # Iterate through rows of actual data
  for row in fileToRead:
    out.append(dict(zip(headers, row)))

  return out
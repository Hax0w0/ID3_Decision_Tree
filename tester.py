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

import ID3
import parse
import random_forest

def main():
 
 # Print out welcome statement
 print("Welcome to the tester for the ID3 Decision Tree")
 print("********************************************************************\n")

 # Get the datasets
 training_data = parse.parse('cars_test.data')
 validation_data = parse.parse('cars_valid.data')
 test_data = parse.parse('cars_train.data')

 # Print out results for decision tree before pruning
 cars_decision_tree = ID3.ID3(training_data, 'acc')
 before_pruning_results = ID3.test(cars_decision_tree, test_data)
 print(f"Accuracy Before Prunning: {before_pruning_results}\n")

 # Print out the results for decision tree after pruning
 ID3.prune(cars_decision_tree, validation_data)
 after_pruning_results = ID3.test(cars_decision_tree, test_data)
 print(f"Accuracy After Prunning: {after_pruning_results}\n")

 # Print out the results for the random forest
 cars_random_forest = random_forest.generate_random_forest(training_data, validation_data)
 random_forest_results = random_forest.test_forest(cars_random_forest, test_data)
 print(f"Accuracy For Random Forest: {random_forest_results}\n")

main()
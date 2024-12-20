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
import random

# Generate_Random_Forest Function
# --------------------------------------------------------------------------------------------
def generate_random_forest(training_data, validation_data):
    '''
    Purpose: Generates a random_forest of that consists of 100 pruned trees.

    Output:
    - Random_Forest: A list of decision trees made by using random sets of the training
                    data (this is done by using bootstrapping).
    '''
    # Initialize forest to return
    random_forest = []

    # Generate 100 trees to put in the forest
    for i in range(100):

        # Use bootstrapping to get subset of the training data
        sample = bootstrap(training_data)
        
        # Create the tree and prune it
        random_forest_tree = ID3.ID3(sample, 1)
        ID3.prune(random_forest_tree, validation_data)

        # Add it to the forest
        random_forest.append(random_forest_tree)

    return random_forest

# Bootstrap Function
# --------------------------------------------------------------------------------------------
def bootstrap(training_data):
    '''
    Purpose: Uses bootstrapping to get a random sample of the training data. Also selects a 
             random subset of the attributes to use for the tree.

    Output:
    - Sample_Bootstrap: A random subset of the training data. Each example only has 3
                        random attributes.
    '''
    # Initialize bootstap sample to return
    sample_bootstrap = []

    # Get the length of the data set
    num_data_points = len(training_data)

    # Get the list of 3 random attributes we want to consider
    all_attributes = list(training_data[0].keys())
    all_attributes.remove('Class')
    sample_attributes = random.sample(all_attributes, 3)

    # Drawing from the data set with replacement
    for i in range(num_data_points):
        random_example = random.choice(training_data).copy()
        construct_example = {}
        construct_example['Class'] = random_example['Class']

        for attribute in sample_attributes:
            construct_example[attribute] = random_example[attribute]
        
        sample_bootstrap.append(construct_example)

    # Return the bootstrapped sample
    return sample_bootstrap

#Test_Forest Function
# --------------------------------------------------------------------------------------------
def test_forest(forest, examples):
    '''
    Purpose: Gives the accuracy of the forest given a list of examples.
    '''
    # Intialize variable to return
    num_correct = 0

    # Get the number of predictions we're making
    num_examples = len(examples)

    # Loop through and get predictions of examples
    for instance in examples:
        prediction = get_forest_prediction(forest, instance)

        if prediction == instance['Class']:
            num_correct += 1

    # Return accuracy
    return num_correct / num_examples

# Get_Forest_Prediction Function
# --------------------------------------------------------------------------------------------
def get_forest_prediction(forest, instance):
    '''
    Purpose: Returns the prediction a forest gives.
    '''
    # Initialize dictionary to store predictions
    predictions = {}

    # Loop through forest to get predictions
    for tree in forest:

        # Get prediction of the tree
        y = ID3.evaluate(tree, instance)

        # Add the prediction to the dictionary
        if y not in predictions:
            predictions[y] = 1
        else:
            predictions[y] = predictions[y] + 1

    # Get the best prediction
    max_count = 0
    best_prediction = None
    for label, count in predictions.items():
        if count > max_count:
            max_count = count
            best_prediction = label

    # Return the best prediction
    return best_prediction


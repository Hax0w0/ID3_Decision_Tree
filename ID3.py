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

import math

# Node Class
# --------------------------------------------------------------------------------------------
class Node:
 '''
 Purpose: The structure of the nodes we'll be using for our tree.
 '''
 def __init__(self, label = None, attribute = None, children = {}, entropy = None):
   
   # The label holds the label of that node.
   self.label = label

   # Attribute is only for inner nodes, describe attribute to split by.
   self.attribute = attribute

   # A dictionary of attribute_value - node pairs (av_1:child_1, av_2:child_2, ...).
   self.children = children

   # Holds the entropy of the examples at this node.
   self.entropy = entropy

# ID3 Function
# --------------------------------------------------------------------------------------------
def ID3(examples, default):
 '''
 Purpose: Takes in examples and returns a decision tree.

 Inputs:
 - Examples: Array of examples (each example is a dictionary of attribute:value pairs).

 Output:
 - Decision tree (an instance of a Node).

 Note:
 - The target class variable is a special attribute with the name "Class".
 - Any missing attributes are denoted with a value of "?".
 '''
 # Initialize the root node
 root_node = Node(None, None, {}, None)

 # Get list of all attributes
 example_keys = examples[0].copy()
 del example_keys['Class']
 attribute_left = list(example_keys.keys())

 # Call the ID3 helper function
 ID3_helper(attribute_left, examples, root_node, default)
 
 # The root node should now contain the tree
 return root_node

# ID3_Helper Function
# --------------------------------------------------------------------------------------------
def ID3_helper(attributes_left, examples, node, default):
 '''
 Purpose: A helper function for the ID3 function that recursively builds the tree.

 Inputs:
 - Attributes_Left: List of attributes left to split with (we don't want to split by the same
                    attribute multiple times in the same branch).
 - Examples: List of examples with their corresponding labels.
 - Node: The current node in the tree.

 Output:
 - None, we are modifying the node of the tree passed in.
 '''
 # Make a copy of the attributes left
 attributes_left_copy = attributes_left.copy()

 # Label the leaf with the label that occurs the most
 node.label = label_leaf(examples, default)

 # Base case where no more attributes are left (node is a leaf)
 if len(attributes_left_copy) == 0:
   node.label = label_leaf(examples, default)
   node.attribute = None
   node.entropy = calculate_entropy(examples)
   node.children = {}
   return
 
 else:
   # Get the best split
   [best_attribute, e_after, split_examples] = get_best_split(examples, attributes_left_copy)

   # Get the entropy of the examples before the split
   node.entropy = calculate_entropy(examples)

   # Calculate the information gain of the best split
   info_gain = calculate_entropy(examples) - e_after

   # If there is no information gain, stop splitting.
   if info_gain <= 0:
     node.label = label_leaf(examples, default)
     node.attribute = None
     node.children = {}
     return
   
   # Otherwise, if there is information gain, perform best split
   attributes_left_copy.remove(best_attribute)

   # Begin making the children for the node
   for attribute_value, split_example in split_examples.items():
      
      # Save the attribute used for the split
      node.attribute = best_attribute

      # Create the child node for each of the groups after the split
      child_node = Node(None, None, {}, None)
      node.children[attribute_value] = child_node
      ID3_helper(attributes_left_copy, split_example, child_node, default)
     
   return

# Label_Leaf Function
# --------------------------------------------------------------------------------------------
def label_leaf(examples, default):
  '''
  Purpose: Takes in a list of examples and returns the label that occurs most frequently. If
           there is a tie, the label should be the default.
  '''
  # Make a dictionary to count all the labels
  label_count = {}

  for example in examples:

      # Get the label of the example
      example_label = example['Class']

      # If this is the first instance of the label, add it to the dictionary
      if example_label not in label_count.keys():
        label_count[example_label] = 1

      # Otherwise, the add 1 to the current count for the label
      else:
        label_count[example_label] = label_count[example_label] + 1

  # Initialize variables to store the most frequent label and highest count
  highest_count = 0
  answer = None

  # Loop through the dictionary to find the most common label
  for label, count in label_count.items():
      
      # If the count is greater than the highest count, update
      if count > highest_count:
        highest_count = count
        answer = label
      
      # If the count is equal to the highest count, update if the label is the default
      elif count == highest_count and label == default:
        answer = label

  return answer

# Calculate_Entropy Function
# --------------------------------------------------------------------------------------------
def calculate_entropy(examples):
 '''
 Purpose: Given a list of examples with their corresponding labels, returns the entropy
          of the given list of examples.

 Inputs:
 - Examples: List of examples with their corresponding labels.

 Output:
 - Entropy: The entropy of the examples.
 '''
 # Create a list to store the total number of occurances for each label
 labels = {}

 # Intialize variable to keep track of the entropy
 entropy = 0

 # Loop throught the examples
 for example in examples:
   
   # Get the label of the example
   label = example['Class']

   # Increase the count of this label in the dictionary
   if label in labels: labels[label] += 1
   else: labels[label] = 1

 # Get the total number of unique labels
 tot_labels = len(examples)

 # Loop through the counts for all the labels
 for label, value in labels.items():
   
   # Calculate the entropy from that label
   entropy -= value / tot_labels * math.log(value / tot_labels, 2)

 return entropy

# Get_Best_Split Function
# --------------------------------------------------------------------------------------------
def get_best_split(examples, attributes_left):
 '''
 Purpose: Given a list of examples with their corresponding labels, returns the entropy
          of the given list of examples.

 Inputs:
 - Examples: List of examples with their corresponding labels.
 - Attributes_Left: List of attributes we could split by.

 Output:
 - Best_Attribute: The best attribute to split by.
 - Min_Entropy: The entropy of the best split we could make.
 - Attribute_Values: A dictionary that has the has the possible values for the attribute
                     we're splitting by for the keys and the list of examples with that
                     value for the attribute for the values.
 '''
 # Intialize variable to store the best attribute to split by
 best_attribute = attributes_left[0]

 # Calculate the entropy and get the groups if we were to split by the first attribute
 [min_entropy, attribute_values] = evaluate_split(examples, attributes_left[0])

 # Loop through all the attributes we could split by
 for attribute in attributes_left:
   
   # Calculate the entropy and the groups if we were to split by the attribute
   [test_entropy, test_attribute_values] = evaluate_split(examples, attribute)

   # If the entropy is better than what we have so far, update what we return.
   if test_entropy < min_entropy:
     min_entropy = test_entropy
     attribute_values = test_attribute_values
     best_attribute = attribute
  
 return [best_attribute, min_entropy, attribute_values]

# Evaluate_Split Function
# --------------------------------------------------------------------------------------------
def evaluate_split(examples, attribute):
 '''
 Purpose: Given a list of examples and an attribute to split by, this function evaluates the
          split by calculating the entropy of the groups. This function also returns the
          groups made by splitting by the specified attribute.

 Inputs:
 - Examples:  A list of examples with their corresponding labels.
 - Attribute: The attribute to split by.

 Output:
 - Entropy: The weighted average antropy of the split groups.
 - Attribute_Values: A dictionary that stores the groups made by splitting by the attribute.
                     It is formatted like {Attribute_Value : Examples}.
 '''
 # Create dictionary to store groups made by splitting by the attribute
 attribute_values = {}

 # Initialize variable for the weighted entropy of the split groups.
 children_entropy = 0
 
 # Get the total number of examples
 total_num_examples = len(examples)

 # Loop through all the examples
 for example in examples:
   
   # Get the label of the example
   label = example['Class']

   # Get the value of the attribute for that example
   example_att_value = example[attribute]

   # If the attribute is missing, skip the datapoint
   if example_att_value == '?':
     total_num_examples -= 1
     continue
   
   # Otherwise, add the example to the group it belongs to
   elif (example_att_value in attribute_values):
     attribute_values[example_att_value].append(example)
   else:
     attribute_values[example_att_value] = [example]

 # If there are no valid examples, we don't want to say this is the best attribute
 if total_num_examples == 0:
  return [math.inf, attribute_values]
   
 # Loop through the groups made by splitting by the specified attribute
 for group in attribute_values.values():
   
   # Calculate the weighted entropy of that group
   group_entropy = calculate_entropy(group)
   weight = len(group) / total_num_examples
   children_entropy += weight * group_entropy

 return [children_entropy, attribute_values]

# Prune Function
# --------------------------------------------------------------------------------------------
def prune(node, examples):
 '''
 Purpose: Takes in a trained tree and a validation set of examples.  Prunes nodes in order to
          improve accuracy on the validation data.
 '''
 # Call the prune_helper function
 prune_helper(node, node, examples)
 
 return

# Prune_Helper Function
# --------------------------------------------------------------------------------------------
def prune_helper(root, node, examples):
  '''
  Purpose: A helper function that prunes the tree using a validation set.

  Inputs:
  - Root: The root of a trained tree.
  - Node: A non-root node of the trained tree.
  - Examples: The validation set of examples.
  '''
  # If there is no splitting attribute, the node is a leaf node
  if node.attribute == None:
    return

  else:
    # Call the prune_helper on each of the children of the node
    for child in node.children.values():
      prune_helper(root, child, examples)

    # Get the accuracy before pruning the children
    accBefore = test(root, examples)

    # Store the attribute used to split and temporarily turn the node into a leaf node
    split_attribute = node.attribute
    node.attribute = None

    # Get the accuracy after pruning the children
    accAfter = test(root, examples)

    # If the accuracy was better before, do not prune.
    if accBefore > accAfter:
      node.attribute = split_attribute

    # Otherwise, prune the children.
    else:
      node.children = {}
      return

  return

# Test Function
# --------------------------------------------------------------------------------------------
def test(node, examples):
 '''
 Purpose: Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
          of examples the tree classifies correctly).
 '''
 # Intialize variable to count the number of correct classifications made
 correct_classifications = 0

 # Loop through the examples
 for example in examples:
   
   # Get the prediction for the example
   result = evaluate(node, example)

   # If the prediction was correct, increase the count of correct classifications
   if result == example['Class']:
     correct_classifications += 1

 # Calculate the accuracy of the tree
 if len(examples) != 0:
    accuracy = correct_classifications / len(examples)
 else:
    print("Empty Dataset") 
    accuracy = 0

 return accuracy

# Evaluate Function
# --------------------------------------------------------------------------------------------
def evaluate(node, example):
 '''
 Purpose: Takes in a tree and one example.  Returns the Class value that the tree
 assigns to the example.
 '''
 # Keep track of the current node
 current_node = node

 # Keep going down the tree until we get to a leaf
 while current_node.attribute is not None:
   
   # Get the value of the attribute the node splits by
   class_value = example[current_node.attribute]

   # If we split by that value, go down that branch
   if class_value in current_node.children:
     current_node = current_node.children[class_value]

   # Otherwise, return the label of the current node of the tree
   else:
     return current_node.label

 # Return the label of the leaf (which is the prediction for the example)
 return current_node.label
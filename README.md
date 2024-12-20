# ID3 Decision Trees README
 **Project**: ID3 Decision Trees + Random Forest<br>
 **Class**: Northwestern CS 349 Fall 2024<br>
 **Contributers**: Raymond Gu, Mimi Zhang, Alxin Xu, Rhema Phiri, Eshan Haq

## ID3 File
The `ID3.py` file contains all the functions and class needed to create a decision tree using the ID3 algorithm.<br>

**Description For Node Class**<br>
The `node` class contains 4 different attributes. The entire decision tree is made up of nodes.<br>
- **Attribute**: The feature / attribute that will be used to split the data. Only inner nodes will have a value for this,
                 leaf nodes will have None for this attribute.<br>
- **Children**: A dictionary where the keys are possible values of the attribute, and the values are the children nodes that
                result from the split. For leaf nodes, this is an empty dictionary.<br>
- **Label**: At every node, we determine the label that occurs most in the training data at that point. Both inner nodes
             and leaf nodes have a value for their label attribute. Inner nodes have a value for this attribute because test
             examples without a value for that attribute or with unseen values for that attribute need a decision for classification.<br>
- **Entropy**: The entropy of the training data at that node.<br><br>

## Random_Forest File
The `random_forest.py` file utilizes the ID3 algorithm in order to create decision trees for a random forest.<br>

**Design Choices**<br>
There were various design choices we made to tailor the random forest for the cars dataset.
- **Resampling**: We decided to use bootstrapping to generate different training subsets. This allows each of the trees to
                  learn slightly different patterns of the data, which helps improve the generalization power of the forest.<br>
- **Random Feature Selection**: For each of our trees in the random forest, we use 3 out of the 7 possible attributes in order
                                to introduce additional randomness and diversity into the model.<br>
- **Number Of Trees**: Our random forest consists of 100 pruned trees.<br><br>

## Parse File
The `parse.py` file was given to us by Professor David Demeter. The purpose of this file was to help parse through the various
cars datasets. Each example in the file is represented as a dictionary, with the feature name mapping to the value of that feature.<br><br>

## Tester File
The `tester.py` file was compares the results on the cars test dataset of the following methods:
- A decision tree without pruning
- A decision tree with pruning
- A random forest with 100 trees

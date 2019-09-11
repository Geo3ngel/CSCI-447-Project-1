""" -------------------------------------------------------------
@file        classifier.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       Contains methods used to classify attributes for data
"""

""" -------------------------------------------------------------
@param  attributes          TODO: Is this a list of every attribute, or? Dana
@param  data                TODO: What kind of data? Dana
@param  attr_to_classify    The given attribute to classify

@return     A hash table in the form of: { <class>: [<matching examples (rows)>] }
            (described in @brief)
@brief      This method creates a dictionary of the classes present for a given attribute
            (form illustrated in @return)
FIXME: Commented out because nothing uses this (Dana)
"""
# import collections
# def separate_data(attributes, data, attr_to_classify):
#     class_idx = attributes.index(attr_to_classify)
#     data_classes = {attr_to_classify:{} }
#     for row_idx in range(len(data)):
#         example = data[row_idx]
#         if example[class_idx] not in data_classes[attr_to_classify]:
#             data_classes[attr_to_classify][example[class_idx]] = []
#         data_classes[attr_to_classify][example[class_idx]].append(example)
#     return data_classes

""" -------------------------------------------------------------
@reference  https://stackoverflow.com/questions/39272862/is-printing-defaultdict-supposed-to-be-ugly-non-human-readable-by-default
Reason: Didn't feel the need to re-invent the wheel.
        Also it is only for data storage purposes.

@brief  Allows for nested keys in a dictionary.
"""
class Tree(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

""" -------------------------------------------------------------
@param  attrs       A list of strings, each representing the name of an attribute
@param  db          A list of examples/samples of a database repository
@param  class_idx   The column number matching an index from @param attrs
                    representing our attribute to classify by

@return    A dictionary in the form of:
           { class -> { attribute -> { response type -> number of such responses }}}}
@brief     Given a Tree object (see above), return a classified data structure
"""

def classify_db(attrs, db, class_idx):
    data_tbl = Tree()

    # For each sample in the database...
    for row in db:

        # Get a count for the current class
        if 'count' not in data_tbl[row[class_idx]].keys():
            data_tbl[row[class_idx]]['count'] = 0
        data_tbl[row[class_idx]]['count'] += 1

        # For each attribute in the current row..
        for attr_idx in range(len(row)):

            # If the current attribute isn't the "class" attribute or the class's count...
            if attr_idx != class_idx and row[attr_idx] != 'count':
                # If the current attribute isn't already in
                # the data_tbl for the current class...
                if row[attr_idx] not in data_tbl[row[class_idx]][attrs[attr_idx]]:
                    # Make the current attribute a key for the current class
                    # and make that attribute's response count
                    data_tbl[row[class_idx]][attrs[attr_idx]][row[attr_idx]] = [0,0]
                
                # Increment the response count by 1
                data_tbl[row[class_idx]][attrs[attr_idx]][row[attr_idx]][0] += 1

    # Return the completed data structure per the form in @return
    return data_tbl

# -----------
# def calc_prob_of_response(raw_data, classified_data):

#     ratios = {}

#     for data_class in classified_data:
#         print(data_class)

# """ -------------------------------------------------------------
# Calculate probabilities for each attribute value
# This is step 2 in the algorithm
# @param data_tbl a data_table created by the classify_db() function
# """
# def calculate_probs(data_tbl):
    # Iterate over each class in data_tbl
    # for classifier, values in data_tbl.items():
    #     for val in values:
    #         if val != 'count':
    #             # Loop thru each value count and calculate the probabilities
    #             for count in data_tbl[classifier][val]:
    #                 data_tbl[classifier][val][count][1] = data_tbl[classifier][val][count][0] / data_tbl[classifier]['count']


# -------------------------------------------------------------
# Old function to calculate attribute probabilities.
# Used the genDataTable function that we no longer have
# 
# import copy
# def calculate_attr_probs(data, attributes, attr_to_classify):
#     # classified_data = separate_data(attributes, data, attr_to_classify)['class']
#     data_table = classify_db(attributes, data, attr_to_classify)
#     prob_table = copy.deepcopy(data_table)
#     for classifier, count_list in prob_table.items():
#         for val, val_counts in count_list.items():
#             for val, count in val_counts.items():
#                 prob = (count + 1) / (len(classified_data[classifier]) + len(attributes))
#                 val_counts[val] = prob

#     return prob_table


# -------------------------------------------------------------
# Guess the class of an example
# @param example a row from the test set that we are trying to classify
# @param training_data_tbl the training data
# @param class_idx the index of the column that stores the class for each row in the data
def calculate_class(example, training_data_tbl, class_idx):
    print("Example: ", example)
    C = [] # Array to store probabilities of each class
    # Iterate over each class in training data table
    for classifier in training_data_tbl:
        prob = 1
        idx = 0
        # Iterate through values for each classifier
        for attr in training_data_tbl[classifier]:
            if attr != 'count':
                if idx != class_idx:
                    if training_data_tbl[classifier][attr][example[idx]][1] != {}:
                        prob *= training_data_tbl[classifier][attr][example[idx]][1]
                    else:
                        prob *= 0
                idx = idx + 1
        C.append(prob)

    print(C)

""" -------------------------------------------------------------
@param  db  The pre-processed data already classified by classify_db()

@return     A dictionary/table of probabilities of each attribute value (i.e. response)
            occuring in each class
@brief      Converts each attribute value/response count into a probability
            of that value occuring within its class.
            IMPORTANT: This is step 3 of "the algorithm"
"""
def calc_prob_of_response(db):

    # For each class in the database...
    for db_class in db:

        # Acquire the total number of classes
        # and remove that value from the local db variable
        class_count = db[db_class].pop('count')
        
        # For each attribute within the class...
        # "Divide the number of examples that match that attribute value (plus one)..."
        # "...by the number of examples in the class (plus d) (d being number of attributes)"
        for attr in db[db_class]:

            for key in db[db_class][attr].keys():
                db[db_class][attr][key][1] = \
                (db[db_class][attr][key][0] + 1) / \
                (class_count + len(db_class))

    return db

'''---------------------------------------------------------
Add noise to the dataset by randomly selecting 10% of the examples
and then shuffling the attribute values around
@param db the database we are adding noise
@param class_idx the the index of the class attribute
@return a deep copy of the database with the noise added
'''
import copy
import math
import numpy as np
def add_noise(db, class_idx):
    noisey_db = copy.deepcopy(db)
    # Get count of 10% of database
    num_rows = math.floor(len(noisey_db.get_data()) * 0.1)
    #Create list of random indices within db
    indices = np.random.random_integers(0, len(noisey_db.get_data())-1, num_rows)
    for idx in indices:
        row = noisey_db.get_data()[idx]
        print("ROW: ", row)
        for i in range(len(row)): # Shuffle values in the current row
            if i == class_idx: #Skip classifier attr.
                continue
            rand_idx = np.random.randint(0,len(row))
            # Make sure we aren't swapping classifier attr. (kinda weird...)
            while(rand_idx == class_idx):
                rand_idx = np.random.randint(0,len(row))
            # swap values
            temp = row[rand_idx]
            row[rand_idx] = row[i]
            row[i] = temp
        print ("SHUFFLED ROW: ", row)
            

                

        


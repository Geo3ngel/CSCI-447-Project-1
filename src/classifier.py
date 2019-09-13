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

def separate_data(attributes, data):
     binSize = int(len(data)/10)
     bin_lengths = []
     row_idx = 0
     return_data = []
     for index in range(10):
         bin_lengths.append(binSize)
     for index in range((len(data)%10 )):
         bin_lengths[index] += 1
     for bin_idx in range(len(bin_lengths)):
        for row in range(bin_lengths[bin_idx]):
            example = data[row_idx]
            return_data.append([bin_idx,*example])
            row_idx += 1
     return [return_data,bin_lengths]

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

'''--------------------------------------------------------------
@param     data    The data Tree, with the class counts included

@return     A set containing the probabilities for each class
@brief      Calculate proportions/probabilities of each class within the data set
'''
def get_class_probs(data):
    Q = [] # Set to store class probs
    total_data = 0 # Will store the total size of the data set
    # For each class in the training data
    for c in data:
        count = data[c]['count']
        total_data += count
        Q.append(count)
    
    Q = [x / total_data for x in Q]
    return Q

# ''' -------------------------------------------------------------
# @param  example     a row from the test set that we are trying to classify
# @param  tbd         the training data table
# @param  class_idx   the index of the column that stores the class for each row in the data

# @return the predicted class
# '''
# import numpy as np
# def calculate_class(example, tbd, class_probs, class_idx):
#     # print("Example: ", example)
#     C = [] # Array to store probabilities of each class

#     # Iterate over each class in training data table
#     for classifier in tbd:
#         prob = 1
#         # idx stores the index of the current attribute of the example
#         # we are evaluating. set to 1, b/c first number in each example 
#         # is the bin number.
#         idx = 1
#         # Iterate through values for each classifier
#         for attr in tbd[classifier]:
#             if attr != 'count':
#                 if idx != class_idx:
#                     if tbd[classifier][attr][example[idx]][1] != {}:
#                         prob *= tbd[classifier][attr][example[idx]][1]
#                     else:
#                         prob *= 0
#                 idx = idx + 1
#         C.append(prob)

#     C = [class_probs[i] * C[i] for i in range(len(C))]
#     return np.argmax(C)

""" -------------------------------------------------------------
@param  db  The pre-processed data already classified by classify_db()

@return     A dictionary/table of probabilities of each attribute value (i.e. response)
            occuring in each class
@brief      Converts each attribute value/response count into a probability
            of that value occuring within its class.
            
            IMPORTANT: This is step 3 of "the algorithm"
"""
def calc_prob_of_response(db):

    # The total number of examples in a database
    sample_size = 0

    # For each class in the database...
    for db_class in db:
        for key, attr in list(db[db_class].items()):

            # This formula doesn't apply to the count probability
            if key != 'count':

                # For each attribute within the class...
                # "Divide the number of examples that match that attribute value (plus one)..."
                # "...by the number of examples in the class (plus d) (d being number of attributes)"
                for val in attr:
                    db[db_class][key][val][1] = \
                    (db[db_class][key][val][0] + 1) / \
                    (db[db_class]['count'] + len(db_class))

            # If we are looking at the count attribute,
            # add it to a generic total
            elif key == 'count':
                sample_size += db[db_class][key]
    
    # We need to re-loop through each class to get
    # each classes probability
    for db_class in db:

        # Probability of a class is it's count divided by the sample size
        temp = []
        temp.append(db[db_class]['count'] )
        temp.append(temp[0] / sample_size)
        db[db_class]['count'] = temp
    
    return db

""" -------------------------------------------------------------
@param  probs               Our data structure containing conditional probabilities
                            of attributes per class (dictionary)
@param  attrs               A list of the names of the attributes in @param data_to_predict
@param  data_to_predict     Our test data subset
@param  db                  Our training data subset
"""
def predict(probs, attrs, data_to_predict, db):
    attribute_indexes = db.get_classifier_attr_cols()
    probs_products = []
    classes = []
    for key in probs.keys():
        probs_products.append(1)
    
    for class_idx, data_class in enumerate(probs):
        classes.append(data_class)
        for attribute_idx in attribute_indexes:
            if attribute_idx != db.get_classifier_col():
                if probs[data_class][attrs[attribute_idx]][data_to_predict[attribute_idx]][1] != {}:
                    probs_products[class_idx] *= probs[data_class][attrs[attribute_idx]][data_to_predict[attribute_idx]][1]
                else:
                    probs_products[class_idx] = 0
    return classes[probs_products.index(max(probs_products))]


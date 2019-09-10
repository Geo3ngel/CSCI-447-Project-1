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

""" -------------------------------------------------------------
@param  raw_data            TODO
@param  classified_data     TODO

@return     TODO (iff this function returns something, else: delete)
@brief      TODO

@reference  https://www.geeksforgeeks.org/iterate-over-a-dictionary-in-python/
            Reason: To learn how to iterate over a dictionary in python
"""
def calc_prob_of_response(raw_data, classified_data):

    ratios = {}

    for data_class in classified_data:
        print(data_class)

""" -------------------------------------------------------------
Calculate probabilities for each attribute value
@param data_tbl a data_table created by the classify_db() function
"""
def calculate_probs(data_tbl):
    # Iterate over each class in data_tbl
    for classifier, values in data_tbl.items():
        for val in values:
            if val != 'count':
                # Loop thru each value count and calculate the probabilities
                for count in data_tbl[classifier][val]:
                    data_tbl[classifier][val][count][1] = data_tbl[classifier][val][count][0] / data_tbl[classifier]['count']

"""-------------------------------------------------------------
Old function to calculate attribute probabilities.
Used the genDataTable function that we no longer have
"""
import copy
def calculate_attr_probs(data, attributes, attr_to_classify):
    # classified_data = separate_data(attributes, data, attr_to_classify)['class']
    data_table = classify_db(attributes, data, attr_to_classify)
    prob_table = copy.deepcopy(data_table)
    for classifier, count_list in prob_table.items():
        for val, val_counts in count_list.items():
            for val, count in val_counts.items():
                prob = (count + 1) / (len(classified_data[classifier]) + len(attributes))
                val_counts[val] = prob

    return prob_table

# Make a dict out of the data_point
# Key is the attribute, value is the val for that attribute in this data point
def prepare_data_point(point, attributes): 
    data_dict = dict()
    for i in range(len(point)):
        data_dict[attributes[i]] = point[i]
    
    return data_dict

def calculate_class(data_point, training_data, classified_data, prob_table, attributes):
    print(data_point)
    classes = prob_table.keys()
    
    Q = dict() # Proportion of dataset for each class
    C = []
    
    for c in classes:
        Q[c] = len(classified_data[c]) / len(training_data)

    for c,v in prob_table.items():
        prob = 1
        for i in range(len(data_point) - 1):
            val = prob_table[c][attributes[i]][data_point[i]]
            if val == {}:
                continue
            else:
                prob = prob * val
        C.append(prob * Q[c])
    
    print(C)
            

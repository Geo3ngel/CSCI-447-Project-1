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
"""
import collections
def separate_data(attributes, data, attr_to_classify):
    # attributes:     ["Foo"..."Bar"]
    # data:           [[1,2,3],[1,2,3]]
    # att_to_classify: "Foo", A string matching the column name, or attribute, of the dataset
    # return { <Attribute to classify by>: { <ClassValue>:[<example or row>] } }
    # Creating a dictionary to hold the class types
    index_of_class = attributes.index(attr_to_classify)
    data_classes = {attr_to_classify:{} }
    for rowIndex in range(len(data)):
        example = data[rowIndex]
        if example[index_of_class] not in data_classes[attr_to_classify]:
            data_classes[attr_to_classify][example[index_of_class]] = []
        data_classes[attr_to_classify][example[index_of_class]].append(example)
    return data_classes
#Referenced/Copied https://stackoverflow.com/questions/39272862/is-printing-defaultdict-supposed-to-be-ugly-non-human-readable-by-default
# User Martineau for how to be able to declare nested keys without using nested if statements
# Didn't feel the need to reinvent the wheel, also it is only for data storage purposes
class Tree(dict):
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

def genDataTable(attributes, data, attr_to_classify):
    dataTable = Tree()
    index_of_class = attributes.index(attr_to_classify)
    for rowIndex in range(len(data)):
        row = data[rowIndex]
        for attributeIndex in range(len(row)) :
                if attributeIndex != index_of_class:
                    if row[attributeIndex] not in dataTable[row[index_of_class]][attributes[attributeIndex]]:
                        dataTable[row[index_of_class]][attributes[attributeIndex]][row[attributeIndex]] = 0
                    dataTable[row[index_of_class]][attributes[attributeIndex]][row[attributeIndex]] = dataTable[row[index_of_class]][attributes[attributeIndex]][row[attributeIndex]] + 1
    return dataTable

# TODO: Come up with a new name for this function?
# TODO: Comment once it's working Dana
# def getNumOfAttributes(subset):
#     # acquire list of attributes
#     attributes = []

#     for a in attributes:
#         getCount()

# def getCount(attribute, data):
#     pass

# TODO:  Finish docstring for this function when convenient Dana
# FIXME: Ratios of what? Describe in @brief? 

""" -------------------------------------------------------------
@param  raw_data            TODO
@param  classified_data     TODO

@return     TODO (iff this function returns something, else: delete)
@brief      TODO

@reference  https://www.geeksforgeeks.org/iterate-over-a-dictionary-in-python/
            Reason: To learn how to iterate over a dictionary in python
"""
def calculate_ratios(raw_data, classified_data):

    ratios = {}

    for data_class in classified_data:
        print(data_class)


import copy
def calculate_attr_probs(data, attributes, attr_to_classify):
    classified_data = separate_data(attributes, data, attr_to_classify)['class']
    data_table = genDataTable(attributes, data, attr_to_classify)
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
            

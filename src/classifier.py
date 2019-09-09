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
    # {'Iris-setosa': {
    #     'sepal length': {'5.1': 8, '4.9': 4, '4.7': 2}, 
    #     'sepal width': {'3.5': 6, '3.0': 6, '3.2': 5, }, 
    #     'petal length': {'1.4': 12, '1.3': 7, '1.5': 14}, 
    #     'petal width': {'0.2': 28, '0.4': 7, '0.3': 7}
    # }
    prob_table = copy.deepcopy(data_table)
    for classifier, count_list in prob_table.items():
        # print(classifier, ": ")
        for val, val_counts in count_list.items():
            # print(val, ": ", val_counts)
            for val, count in val_counts.items():
                prob = count / (len(classified_data[classifier]) + len(attributes))
                val_counts[val] = prob

    print(prob_table)        

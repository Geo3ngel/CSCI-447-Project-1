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
                probs_products[class_idx] *= probs[data_class][attrs[attribute_idx]][data_to_predict[attribute_idx]][1]
    return classes[probs_products.index(max(probs_products))]


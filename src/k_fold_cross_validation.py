""" -------------------------------------------------------------
@file        k_fold_cross_validation.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       Contains all functionality related to k-fold cross-validation
"""

import classifier
from copy import deepcopy
from loss_functions import *
import process_data

""" -------------------------------------------------------------
@param  k                   The number of folds we are using for k-fold cross validation
@param  binned_data_set     A list of examples/samples of a database repository
@param  bin_lengths         A list containing the lengths of each bin, the index in the list is 

@return    binned_guess_results: [[<incorrect_guesses>, <correct_guesses>]]
                incorrect_guesses: [[expected answer,incorrect guess]]
                correct_guesses: [correct guess] 

@brief     Given a number of folds k, and binned data, as well as bin_lengths,
           iterate over each bin and separate the data into two subsets, 
           training data and test_data. 
           Then classify the training data and calculate the probabilities.
           Run prediction on each row of the test_data set and return
           an array of guess results containing
           guess results associated with each bin,
           as every bin will be the test bin at some point.
"""
def k_fold(k,binned_data_set,bin_lengths, db, shuffle):
    #print (binned_data_set)
    binned_guess_results = []
    percent_correct_bins = []
    attr_headers = db.get_attr()
    class_list = db.get_classifiers()
    precision_values = []
    recall_values = []
    # For each bin in our data
    for bin_number in range(k):
        incorrect_guesses = []
        correct_guesses = []
        test_data = []
        training_data = deepcopy(binned_data_set)
        row_idx = 0
        # Add rows from the main data set to our test_data subset until it is the length of the bin that we are using as our test bin (This is to ensure we stop after finding all of the rows that match the bin we want to use)
        while len(test_data) < bin_lengths[bin_number]:
            if training_data[row_idx][0] == bin_number:
                test_data.append(training_data.pop(row_idx).copy()[1:])
                row_idx -=1
            row_idx += 1

        #Remove the bin numbers from our training data, this is done because our classifier does not support bin numbers
        for row_idx2 in range(len(training_data)):
            training_data[row_idx2].pop(0)

        if shuffle:
            training_data = process_data.shuffle_all(training_data,.1)
        # Classify our training data set, so we can calculate the probabilites
        classified_training_data = classifier.classify_db(attr_headers, training_data, db.get_classifier_col())

        # Calculate the probabilities
        training_probs = classifier.calc_prob_of_response(classified_training_data)

        # For each row (sample) in our test_data, try to predict its class
        for test_row in test_data:
            predicted = classifier.predict(training_probs, attr_headers, test_row, db)
            
            # If the class is guessed correctly, append the value to the correct_guesses list
            if  predicted== test_row[db.get_classifier_col()]:
                correct_guesses.append(predicted)
            # If the class is guessed incorrectly, append both the expected and predicted value to the incorrect_guesses list
            else:
                incorrect_guesses.append([test_row[db.get_classifier_col()],predicted])
                
        binned_guess_results.append([incorrect_guesses,correct_guesses])
        recall_values.append(recall_non_binary([incorrect_guesses, correct_guesses], class_list))
        precision_values.append(precision_non_binary([incorrect_guesses,correct_guesses], class_list))
        percent_correct_bins.append(len(correct_guesses)/(len(incorrect_guesses)+len(correct_guesses)))
        
    PRECISION = sum(precision_values) / len(precision_values)
    RECALL = sum(recall_values) / len(recall_values)
    # print("PRECISION: ", sum(precision_values) / len(precision_values))
    # print("RECALL: ", sum(recall_values) / len(recall_values))
    return PRECISION, RECALL, (sum(percent_correct_bins)/len(percent_correct_bins))
    
        
    #print(" \n \n \n Binned Guess Results\n \n \n")
    #print(binned_guess_results)
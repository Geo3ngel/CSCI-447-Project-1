import classifier
from copy import deepcopy

""" -------------------------------------------------------------
@param  k                   The number of folds we are using for k-fold cross validation
@param  binned_data_set     A list of examples/samples of a database repository
@param  bin_lengths         A list containing the lengths of each bin, the index in the list is 

@return    binned_guess_results: [[<incorrect_guesses>, <correct_guesses>]]
                incorrect_guesses: [[expected answer,incorrect guess]]
                correct_guesses: [correct guess] 
@brief     Given a number of folds k, and binned data, as well as bin_lengths, iterate over each bin and separate the data into two subsets, training_data and test_data. 
           Then classify the training data and calculate the probabilities. Run prediction on each row of the test_data set and return an array of guess results containing guess results
           associated with each bin, as every bin will be the test bin at some point.
"""
def k_fold(k,binned_data_set,bin_lengths, db):
    #print (binned_data_set)
    binned_guess_results = []
    attr_headers = db.get_attr()
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

        # Classify our training data set, so we can calculate the probabilites
        classified_training_data = classifier.classify_db(attr_headers, training_data, 0)

        # Calculate the probabilities
        training_probs = classifier.calc_prob_of_response(classified_training_data)

        # For each row (sample) in our test_data, try to predict its class
        for test_row in test_data:
            predicted = classifier.predict(training_probs, attr_headers, test_row, db)
            
            # If the class is guessed correctly, append the value to the correct_guesses list
            if  predicted== test_row[0]:
                correct_guesses.append(predicted)
            # If the class is guessed incorrectly, append both the expected and predicted value to the incorrect_guesses list
            else:
                incorrect_guesses.append([test_row[0],predicted])
                
        binned_guess_results.append([incorrect_guesses,correct_guesses])
        print('\n \n \n Correct Guesses: \n \n')
        print(len(correct_guesses))
        print('\n \n \n Incorrect Guesses: \n \n')
        print(len(incorrect_guesses))
        print(" \n \n \n training probs \n \n \n" + str(training_probs))

    print(binned_guess_results)
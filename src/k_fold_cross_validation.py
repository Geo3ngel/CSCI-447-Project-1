import classifier
from copy import deepcopy

def k_fold(k,binned_data_set,bin_lengths):
    #print (binned_data_set)
    incorrect_guesses = []
    correct_guesses = []
    temp_attr_headers = ['pol','a2','a3','a4','a5','a6','a7','a8','a9','a10','a11','a12','a13','a14','a15','a16','a17']
    #classified_data = classifier.classify_db(temp_attr_headers, repaired_db, 0)
    for bin_number in range(k):
        test_data = []
        print("\n \n BINNED DATA SET")
        print(binned_data_set)
        training_data = deepcopy(binned_data_set)
        row_idx = 0
        print(" \n \nTraining Data Set \n \n")
        print(training_data)
        while len(test_data) < bin_lengths[bin_number]:
            #print("len Test_Data " + str(len(test_data)))
            #print("bin length " + str(bin_lengths[bin_number]))
            #print("row" + str(row_idx))
            if training_data[row_idx][0] == bin_number:
                test_data.append(training_data.pop(row_idx).copy()[1:])
                row_idx -=1
            row_idx += 1

        for row_idx2 in range(len(training_data)):
            training_data[row_idx2].pop(0)

        
        classified_training_data = classifier.classify_db(temp_attr_headers, training_data, 0)
        training_probs = classifier.calc_prob_of_response(classified_training_data)
        for test_row in test_data:
            predicted = classifier.predict(training_probs, ['a2','a6'], temp_attr_headers, test_row)
            if  predicted== test_row[0]:
                correct_guesses.append([predicted])
            else:
                incorrect_guesses.append([test_row[0],predicted])

        print('\n \n \n Correct Guesses: \n \n')
        print(len(correct_guesses))
        print('\n \n \n Incorrect Guesses: \n \n')
        print(len(incorrect_guesses))
        print(" \n \n \n training probs \n \n \n" + str(training_probs))
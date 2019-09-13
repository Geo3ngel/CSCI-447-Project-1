import numpy as np
from classifier import *
from k_fold_cross_validation import *
import os
import process_data
from path_manager import pathManager as pm

def precision_binary(TP, FP):
    return TP / (TP + FP)

def recall_binary(TP, FN):
    return TP / TP + FN

'''
binned_guess_results: [[<incorrect_guesses>, <correct_guesses>]]
incorrect_guesses: [[expected answer,incorrect guess]]
correct_guesses: [correct guess]
'''
guess_results = [
    #bin 1:
    [
        #incorrect guesses:
        [['republican', 'democrat'], ['democrat', 'republican'], ['democrat', 'republican']],
        #correct guesses:
        ['republican', 'democrat', 'democrat', 'republican']
    ]
]
#bin:
bin_results = [
    [['republican', 'democrat'], ['democrat', 'republican'], ['democrat', 'republican']],
    ['republican', 'democrat', 'democrat', 'republican', 'republican']
]

classes = ['republican', 'democrat']
# Get true positive guesses
def true_positives(bin_results, classes):
    correct = bin_results[1]
    TP = [0 for i in range(len(classes))]
    for guess in correct:
        TP[classes.index(guess)] += 1
    return TP

# Get false positive guesses
def false_positives(bin_results, classes):
    incorrect_guesses = bin_results[0]
    FP = [0 for i in range(len(classes))]
    for guess in incorrect_guesses:
        FP[classes.index(guess[1])] += 1
    return FP


# Get false negative guesses
def false_negatives(bin_results, classes):
    incorrect_guesses = bin_results[0]
    FN = [0 for i in range(len(classes))]
    for guess in incorrect_guesses:
        FN[classes.index(guess[0])] += 1
    return FN

print("True Positives: ", true_positives(bin_results, classes))
print("False Positives: ", false_positives(bin_results, classes))
print("False Negatives: ", false_negatives(bin_results, classes))


'''----------------------------------------
@param  bin_results the set of guesses for the current bin
@param  classes     a set of the class names for the current dataset
@return the precision score for this current bin
'''
def precision_non_binary(bin_results, classes):
    TP = true_positives(bin_results, classes)
    FP = false_positives(bin_results, classes)

    precision = 0
    
    for i in range(len(TP)):
        precision += TP[i] / (TP[i] + FP[i])
    
    return  (1 / len(TP)) * precision

'''----------------------------------------
@param  bin_results the set of guesses for the current bin
@param  classes     a set of the class names for the current dataset
@return the recall score for this current bin
'''
def recall_non_binary(TP, FN):
    recall = 0
    
    for i in range(len(TP)):
        recall += TP[i] / (TP[i] + FN[i])
    
    return (1 / len(TP)) * recall

# path_manager = pm()
# path_manager.set_current_selected_folder('iris')
# db = process_data.process_database_file(path_manager)
# normal_data, irregular_data = process_data.identify_missing_data(db.get_data(), 'sepal width in cm')


# attrs = ["sepal length", "sepal width", "petal length", "petal width", "class"]

# classified_data = classify_db(attrs, normal_data, 4)
# class_probs = get_class_probs(classified_data)
# classified_data = calc_prob_of_response(classified_data)

# binified_data = separate_data(attrs, db.get_data(), 'class')
# classes = ['Iris-setosa', 'Iris-versicolor', 'Iris-verginica']


# k_fold(10, classifier.separate_data(attrs,db.get_data())[0],classifier.separate_data(attrs,db.get_data())[1])


# for row in binified_data:
#     if row[0] == 9:
#         # Let's start guessing!
#         print("ROW: ", row)
#         idx = calculate_class(row, classified_data, class_probs, 5)
#         print("GUESSED CLASS: ", classes[idx])
#         print("------------------------------")




import numpy as np
from classifier import *
import os
import process_data
from path_manager import pathManager as pm

""" -------------------------------------------------------------
@param  prob  The probability of the guessed attribute value being correct
              given the likelihood provided by the given attributes' conditional probabilities

@return       The negative natural logarithm of @param prob
@brief        An implementation of a cross entropy loss function
"""
def cross_entropy(prob):
    return -np.log(prob)

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
        if TP[i] == 0 and FP[i] == 0:
            precision += 0
        else:
            precision += TP[i] / (TP[i] + FP[i])
    return  (1 / len(TP)) * precision

'''----------------------------------------
@param  bin_results the set of guesses for the current bin
@param  classes     a set of the class names for the current dataset
@return the recall score for this current bin
'''
def recall_non_binary(bin_results, classes):
    TP = true_positives(bin_results, classes)
    FN = false_negatives(bin_results, classes)
    recall = 0
    
    for i in range(len(TP)):
        if FN[i] == 0 and TP[i] == 0:
            recall += 0
        else:
            recall += TP[i] / (TP[i] + FN[i])
    
    return (1 / len(TP)) * recall


#bin:
bin_results = [
    [
        ['republican', 'democrat'], 
        ['democrat', 'republican'], 
        ['democrat', 'republican']
    ],
    ['republican', 'democrat', 'democrat', 'republican', 'republican']
]

classes = ['republican', 'democrat']

# print(precision_non_binary(bin_results, classes))
# print(recall_non_binary(bin_results, classes))




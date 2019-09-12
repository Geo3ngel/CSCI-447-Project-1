import numpy as np
# from classifier import classify_db, calculate_class, calc_prob_of_response, separate_data
from classifier import *
import os
import process_data
from path_manager import pathManager as pm

def precision_binary(TP, FP):
    return TP / (TP + FP)

def recall_binary(TP, FN):
    return TP / TP + FN

'''----------------------------------------
Calculate precision for data with non-binary classification
@param TP - set of true positive counts, i.e. the number, for each class, of
examples that were correctly classifified. TP[i] = number of examples correctly 
classified as class i
@param FP - set of false positive counts
'''
def precision_non_binary(TP, FP):
    precision = 0
    
    for i in range(len(TP)):
        precision += TP[i] / (TP[i] + FP[i])
    
    return  (1 / len(TP)) * precision

# FP = [2,3,4]
# TN = [1,6,7]
def recall_non_binary(TP, FN):
    recall = 0
    
    for i in range(len(TP)):
        recall += TP[i] / (TP[i] + FN[i])
    
    return (1 / len(TP)) * recall

path_manager = pm()
path_manager.set_current_selected_folder('iris')
db = process_data.process_database_file(path_manager)
normal_data, irregular_data = process_data.identify_missing_data(db.get_data(), 'sepal width in cm')


attrs = ["sepal length", "sepal width", "petal length", "petal width", "class"]

classified_data = classify_db(attrs, normal_data, 4)
class_probs = get_class_probs(classified_data)
classified_data = calc_prob_of_response(classified_data)

binified_data = separate_data(attrs, db.get_data(), 'class')

for row in binified_data:
    if row[0] == 0:
        # Let's start guessing!
        print("ACTUAL ROW:")




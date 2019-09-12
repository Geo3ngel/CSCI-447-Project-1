import numpy as np
from classifier import classify_db, calculate_class, calc_prob_of_response
import os
import process_data
from path_manager import pathManager as pm

def precision_binary(TP, FP):
    return TP / (TP + FP)

def recall_binary(TP, FN):
    return TP / TP + FN

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
training_data = calc_prob_of_response(classified_data)
print(training_data)

# calculate_class(normal_data[0], training_data, 4)



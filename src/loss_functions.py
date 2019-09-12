import numpy as np

def precision_binary(TP, FP):
    return TP / (TP + FP)

def recall_binary(TP, FN):
    return TP / TP + FN

def precision_non_binary(TP, FP):
    precision = 0
    for i in range(len(TP)):
        precision += TP[i] / (TP[i] + FP[i])
    return  (1 / len(TP)) * precision

def recall_non_binary(TP, FN):
    recall = 0
    for i in range(len(TP)):
        recall += TP[i] / (TP[i] + FN[i])
    
    return (1 / len(TP)) * recall




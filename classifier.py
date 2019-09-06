
import numpy as np

def separateData(attributes, data, attToClassify):
    """
    [[1,2,3],[1,2,3]]
    """
    # attributes: ["Foo"..."Bar"]
    # data: [[1,2,3],[1,2,3]]
    # attToClassify: "Foo", A string matching the column name, or attribute, of the dataset
    # Creating a dictionary to hold the class types
    indexOfAttribute = attributes.index(attToClassify)
    dataClasses = {}
    for i in range(len(data)):
        example = data[i]
        if example[indexOfAttribute] not in dataClasses:
            dataClasses[example[indexOfAttribute]] = []
        dataClasses[example[indexOfAttribute]].append(example)
    return dataClasses


def attributeCount(subset): #TODO find a better name for this function
    # get dimensions of subset
    rows, cols = subset.shape
    for col in subset.T:
        for val in col:
            # https://ask.sagemath.org/question/10279/frequency-count-in-numpy-array/
            # got this count method from above link
            count = list(col).count(val)
            print(val, ': ', count) 
        print('----------')
    # for a in attributes:
    #     getCount(a, subset)


def getCount(attribute, data):
    return 1


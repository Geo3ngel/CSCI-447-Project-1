from classifier import separateData, attributeCount
import numpy as np

dataset = [[1,20,1], [2,21,0], [3,22,1]]
#print(separateData(["apples","bananas", "oranges"],dataset,"oranges"))

subset = np.array([ #test subset I'm using
    [1, 20, 1],
    [3, 22, 1],
    [5, 9, 1],
    [2, 6, 1],
    [1, 4, 1],
    [5, 6, 1]
])

attributeCount(subset)





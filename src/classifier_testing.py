from classifier import separate_data, genDataTable, calculate_attr_probs
# from classifier import genDataTable
import os
import process_data
from path_manager import pathManager as pm


# dataset = [["y","n","Democrat"], ["n","y","Republican"], ["n","n","Democrat"]]
# print(separate_data(["q1","q2", "Classes"],dataset,"Classes"))
# print(genDataTable(["q1","q2", "Classes"],dataset,"Classes"))


full_path = "/Users/admin/Desktop/2019 Fall Semester/Machine Learning/CSCI-447-Project-1/databases/iris/iris.data"
db = process_data.process_database_file(full_path)

normal_data, irregular_data = process_data.identify_missing_data(db.get_data())
normal_data = normal_data[0:len(normal_data)-1] # last row is empty so the code wasn't running

attrs = ["sepal length", "sepal width", "petal length", "petal width", "class"] 
classified_data = separate_data(attrs, normal_data, "class")['class']

# This prints the separated data with clean formatting
# for c in classified_data:
#     print(c)
#     for inst in classified_data[c]:
#         print(inst)

# print(len(classified_data['Iris-setosa']))

data_table = genDataTable(attrs, normal_data, 'class')
# This prints the data_table with clean formatting
# for clss in data_table:
#     print(clss)
#     for inst in data_table[clss]:
#         print(inst, ": ", data_table[clss][inst])

calculate_attr_probs(normal_data, attrs, 'class')








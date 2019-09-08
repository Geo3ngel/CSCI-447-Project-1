from classifier import separate_data
from classifier import genDataTable
dataset = [["y","n","Democrat"], ["n","y","Republican"], ["n","n","Democrat"]]
print(separate_data(["q1","q2", "Classes"],dataset,"Classes"))
print(genDataTable(["q1","q2", "Classes"],dataset,"Classes"))
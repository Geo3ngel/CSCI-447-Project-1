from classifier import classify_db
dataset = [["y","n","Democrat"], ["n","y","Republican"], ["n","n","Democrat"]]
print(classify_db(["q1","q2", "Classes"],dataset,2))
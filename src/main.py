""" -------------------------------------------------------------
@file        main.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       The file that runs the program
"""
import os
import process_data
import classifier
import k_fold_cross_validation
from path_manager import pathManager as pm

# Asks for user to select a database from a list presented from current database collection directory.
def select_database(databases):
    
    if len(databases) == 0:
        print("ERROR: No databases found!")
        return False
    
    chosen = False
    database = ""
    
    # Selection loop for database
    while(not chosen):
        print("\nEnter one of the databases displayed:", databases)
        database = input("Entry: ")
        if database in databases:
            print("Selected:", database)
            chosen = True
        else:
            print(database, "is an invalid entry. Try again.")
        
    return database

# Cleaner print outs for the sake of my sanity.
def print_database(database):
    
    if len(database) < 1:
        print("[] - Empty")
    else:
        for row in database:
            print(row)

# Initializes path manager with default directory as databases.
path_manager = pm()

# Loads in a list of database folders for the user to select as the current database.
selected_database = select_database(path_manager.find_folders(path_manager.get_databases_dir()))

# Sets the selected database folder in the path manager for referencing via full path.
path_manager.set_current_selected_folder(selected_database)

# Processes the file path of the database into a pre processed database ready to be used as a learning/training set.
db = process_data.process_database_file(path_manager)

# ### Sanity checks. TODO: move to a unit test case file.
normal_data, irregular_data = process_data.identify_missing_data(db)

corrected_data = process_data.extrapolate_data(normal_data, irregular_data, db.get_missing_symbol())
# print("\nNormal Data:")
# print_database(normal_data)

# -------------------------------------------------------------

#print("\n\n\n\n\nIrregular Data:")
#print_database(irregular_data)

# -------------------------------------------------------------

# print("\n\n\n\n\nCorrected Irregular Data:")
# print_database(corrected_data)
#print("Irregular data total:", len(irregular_data))
#print("Regular data total:", len(normal_data))
#rint("Corrected data total:", len(corrected_data))

# repaired_db is the total database once the missing values have been filled in.
if len(corrected_data) > 0:
    repaired_db = normal_data + corrected_data
else:
    repaired_db = normal_data
    
db.set_data(repaired_db)

process_data.convert(db.get_data())

#print("\n\n\nFINAL DATABASE:\n\n\n")
#print_database(db.get_data())
# # -------------------------------------------------------------

# print("\nRunning classifier...")
# print('\n\n\n\n\nRunning classify_db():')
binned_data = classifier.separate_data(db.get_attr(),db.get_data())
print('\n \n \n Pre-shuffle 0/1 loss: ')
print(k_fold_cross_validation.k_fold(10,binned_data[0],binned_data[1], db, False))
print('\n \n \n Post-shuffle 0/1 loss: ')
print(k_fold_cross_validation.k_fold(10,binned_data[0],binned_data[1], db, True))


# classified_data = classifier.classify_db(temp_attr_headers, repaired_db, 0)

# print(classified_data)

# print("\n\nRunning calc_prob_of_response():")
# probs = classifier.calc_prob_of_response(classified_data)
# print('\n\nprobs:\n')
# print(probs)
# print('\n\nprobs Products:\n')
# print(classifier.predict(probs,['a2'],temp_attr_headers,repaired_db[0]))
print("\nFinished.")
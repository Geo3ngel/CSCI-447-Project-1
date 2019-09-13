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

# Sanity checks.
normal_data, irregular_data = process_data.identify_missing_data(db)

corrected_data = process_data.extrapolate_data(normal_data, irregular_data, db.get_missing_symbol())

# repaired_db is the total database once the missing values have been filled in.
if len(corrected_data) > 0:
    repaired_db = normal_data + corrected_data
else:
    repaired_db = normal_data
    
db.set_data(repaired_db)

process_data.convert(db.get_data())

binned_data = classifier.separate_data(db.get_attr(),db.get_data())
print("\n \n Input Data Structure:")
print('---------------------')
print(db.get_data()[0:10])
print('\n \n Pre-shuffle')
print('---------------------')
pre_shuffle = k_fold_cross_validation.k_fold(10,binned_data[0],binned_data[1], db, False)
print("0/1 Loss: ", pre_shuffle[0])
print('\n \n Post-shuffle')
print('---------------------')
post_shuffle = k_fold_cross_validation.k_fold(10,binned_data[0],binned_data[1], db, True)
print("0/1 Loss: ", post_shuffle[0])
print("\n \n Probability Data Structure:")
print('---------------------')
print(post_shuffle[1])
print("0/1 Loss: ", post_shuffle)

print("\nFinished.")
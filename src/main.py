""" -------------------------------------------------------------
@file        main.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       The file that runs the program
"""
import process_data
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
        print("Enter one of the databases displayed:", databases)
        database = input("Database: ")
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

print("Starting...")
# TODO: Enter user input for pathing. -George
# TODO: Make pathing manager for choosing database -George
db = process_data.process_database_file("../databases/breast-cancer-wisconsin/breast-cancer-wisconsin.data")

# Initializes path manager with default directory as databases.
path_manager = pm()

# TODO: select target for data read in!
print(path_manager.get_databases_dir())
print("Databases: \n", path_manager.find_folders(path_manager.get_databases_dir()))
select_database(path_manager.find_folders(path_manager.get_databases_dir()))

normal_data, irregular_data = process_data.identify_missing_data(db.get_data())

# print("\nNormal Data:")
# print_database(normal_data)

# print("\nIrregular Data:")
# print_database(irregular_data)

# print("\nFinished.")
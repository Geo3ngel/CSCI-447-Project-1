""" -------------------------------------------------------------
@file        main.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       The file that runs the program
"""
# TODO: Turn the contents of this file into unit tests.
import process_data
from path_manager import pathManager as pm

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

normal_data, irregular_data = process_data.identify_missing_data(db.get_data())

print("\nNormal Data:")
print_database(normal_data)

print("\nIrregular Data:")
print_database(irregular_data)

print("\nFinished.")

test = pm()
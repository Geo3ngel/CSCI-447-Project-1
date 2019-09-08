""" -------------------------------------------------------------
@file        process_data.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       Imports and pre-processes data repositories
"""

from database import database as db
import random

""" -------------------------------------------------------------
@param  input_database  The database file (of type .data) to be processed

@return     The pre-processed data from input_db as a database object
            (see database.py)
@brief      Loads the file contents into a database object
"""
# FIXME: Change to use numpy for efficiency's sake?
def process_database_file(input_db):

    current_db_file = open(input_db, 'r')
    db_data = []

    for line in current_db_file:
        # Converts the string line from the file into a set of values.
        db_data.append(csv_to_set(line))
            
    current_db_file.close()

    return db(db_data)

""" -------------------------------------------------------------
@param  input_csv   Comma-seperated string to convert

@return     A set of values found in input_csv
@brief      Converts comma seperated strings into a set of values
"""
def csv_to_set(input_csv):
    return input_csv.strip('\n').split(',')

""" -------------------------------------------------------------
@param  database        Input database to operate upon per @brief
@param  attribute_count The amount of expected attributes for each row of data.

@return     input_db, correction_que : returns the 'clean' rows of data (input_db), and the rows of any malformed data (correction_queue).
            PS: You aren't dumb Dana -George
@brief      Either removes data with missing parameters,
            or extrapolates missing data using bootstraping methodology.
"""
def data_correction(input_db, attribute_count):
    
    # Holds the rows of data that appear to be missing some attributes
    correction_queue = []
    
    # Checks if the data from a specific row
    # has all of the required parameters.
    # If not, pops it from the list into a later processing queue.
    for data in input_db:
        if len(data) is not attribute_count:
            correction_queue.append(data)
            input_db.remove(data)
            
    return input_db, correction_queue

# Finds any ambiguous/missing data and returns the rows of the relevant database in which missing parameters occur.
def identify_missing_data(input_db):
    
    # Holds the rows of data that appear to be missing some attributes
    correction_queue = []
    normal = []
    for data in input_db:
        
        # Check for a missing parameter character:
        if "?" in data:
            # Adds data to que for correction
            correction_queue.append(data)
        else:
            # Adds data to normal database (won't have to be modified further via extrapolation)
            normal.append(data)
            
    return normal, correction_queue

def extrapolate_data(normal_data, malformed_data):
    corrected_data = []
    
    for data in malformed_data:
        corrected_data.append(bootstrap_selection(normal_data, data))
        
    return corrected_data
    
# Deal with missing attributes
    # If 'low' number of missing attributes: remove.
    # Else: Generate a random attribute from a pool of prexisting ones?
        # Set up a queue of lines that need to do this, so we have the pool already fully generated.
            # TODO: DOCUMENT THIS CHOICE.
            
# Fills in the unknown/missing data from existing normal data randomly.
def bootstrap_selection(normal_data, malformed_row):
    length = len(malformed_row)
    
    corrected_data = []
    
    for index in range(length):
        if malformed_row[index] is "?":
            corrected_data.append(random.choice(normal_data)[index])
        else:
            corrected_data.append(malformed_row[index])
            
    return corrected_data
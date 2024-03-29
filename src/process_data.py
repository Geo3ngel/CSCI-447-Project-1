""" -------------------------------------------------------------
@file        process_data.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       Imports and pre-processes data repositories
"""

from database import database as db
import random
import os

""" -------------------------------------------------------------
@param  input_database  The database file (of type .data) to be processed

@return     The pre-processed data from input_db as a database object
            (see database.py)
@brief      Loads the file contents into a database object
"""

def process_database_file(path_manager):

    # loads in data file from the selected database directory
    data_filename = path_manager.find_files(path_manager.get_current_selected_dir(), ".data")[0]
    full_data_path = os.path.join(path_manager.get_current_selected_dir(), data_filename)

    current_db_file = open(full_data_path, 'r')
    db_data = []

    for line in current_db_file:
        # Converts the string line from the file into a set of values.
        db_data.append(csv_to_set(line))
            
    current_db_file.close()
    
    if len(db_data[-1]) < 0:
        db_data.pop()
    elif db_data[-1][0] is "" and len(db_data[-1]) is 1: 
        db_data.pop()
        

    
    attributes, classifier_column, classifier_attr_cols, missing_symbol = read_attributes(path_manager.get_current_selected_dir(), data_filename)

    return db(db_data, attributes, classifier_column, classifier_attr_cols, missing_symbol)

# Reads in the attribute file from a database, and returns the attributes as a list
def read_attributes(directory, data_filename):
    attribute_file_name = data_filename[:-4] + "attr"
    
    full_path = os.path.join(directory, attribute_file_name)
    
    attribute_file = open(full_path, 'r')
    
    # Reads in attributes from line 1 and split/cleans into list
    attributes = attribute_file.readline().strip('\n').split(',')
    
    # Reads in the index of the Classifier column.
    classifier_column = int(attribute_file.readline().strip('\n'))
    
    # Reads in the indexes of the attributes used for classification
    classifier_attr_cols = []
    for cols in  attribute_file.readline().strip('\n').split(','):
        classifier_attr_cols.append(int(cols))
        
    missing_symbol = attribute_file.readline().strip('\n')
    
    return attributes, classifier_column, classifier_attr_cols, missing_symbol
    
""" -------------------------------------------------------------
@param  input_csv   Comma-seperated string to convert

@return     A set of values found in input_csv
@brief      Converts comma seperated strings into a set of values
"""
def csv_to_set(input_csv):
    return input_csv.strip('\n').split(',')

# Goes over the database and runs necessary conversions.
def convert(database):
    if len(database) > 0:
        attribute_count = len(database[0])
        for attribute_col in range(0, attribute_count):
            if needs_conversion(database, attribute_col):
                # TODO: return if needed
                database = equal_width_conversion(database, attribute_col)
                

# Returns a boolean value representative of whether or not the column of values needs to be converted from quantitative to catagorial.
def needs_conversion(database, attribute_col):
    for data_row in database:
        # See if the value for each row of the column specified is a float/int
        try:
            float(data_row[attribute_col])
        except ValueError:
            return False
    return True

# Converts a column of quantitative data to catagorical values.
def equal_width_conversion(database, attribute_col):
    
    bin_count = 3
    
    min = float(database[0][attribute_col])
    max = float(database[0][attribute_col])
    
    # find the largest & smallest values
    for data_row in database:
        if float(data_row[attribute_col]) > max:
            max = float(data_row[attribute_col])
        elif float(data_row[attribute_col]) < min:
            min = float(data_row[attribute_col])
            
    # Calculate binning width
    width = (max - min)/bin_count

    small_bin = []
    medium_bin = []
    large_bin = []
    # Put data in bins
    for data_row in database:
        if min <= float(data_row[attribute_col]) < (min+width):
            small_bin.append(data_row)
        elif (min+width) <= float(data_row[attribute_col]) < (min+(2*width)):
            medium_bin.append(data_row)
        elif (min+(2*width)) <= float(data_row[attribute_col]) <= (max):
            large_bin.append(data_row)
            
    # Overwrites small bin values
    for data_row in small_bin:
        data_row[attribute_col] = str(min)+"-"+str(min+width)
    
    for data_row in medium_bin:
        data_row[attribute_col] = str(min+width)+"-"+str(min+(2*width))
        
    for data_row in large_bin:
        data_row[attribute_col] = str(min+(2*width))+"-"+str(max)
        
    merged_bins = small_bin + medium_bin
    merged_bins += large_bin
    
    return merged_bins
        
""" -------------------------------------------------------------
@param  database           Input database to operate upon per @brief
@param  attribute_count    The amount of expected attributes for each row of data.

@return     input_db, correction_que :
            returns the 'clean' rows of data (input_db),
            and the rows of any malformed data (correction_queue).

@brief      Either removes data with missing parameters,
            or extrapolates missing data using bootstraping methodology.
"""
def data_correction(input_db, attribute_count):
    
    # Holds the rows of data that appear to be missing some attributes
    correction_queue = []
    
    # Checks if the data from a specific row
    # has all of the required parameters.
    # If not, pops it from the list into a later processing queue.
    for data in input_db.get_data():
        if len(data) is not attribute_count:
            correction_queue.append(data)
            input_db.remove(data)
            
    return input_db, correction_queue

# Finds any ambiguous/missing data and returns the rows of the relevant database in which missing parameters occur.
def identify_missing_data(input_db):
    
    # Holds the rows of data that appear to be missing some attributes
    correction_queue = []
    normal = []
    for data in input_db.get_data():
        
        # Check for a missing parameter character:
        if input_db.get_missing_symbol() in data:
            # Adds data to que for correction
            correction_queue.append(data)
        else:
            # Adds data to normal database (won't have to be modified further via extrapolation)
            normal.append(data)
            
    return normal, correction_queue

def extrapolate_data(normal_data, malformed_data, missing_data_val):
    corrected_data = []
    
    for data in malformed_data:
        corrected_data.append(bootstrap_selection(normal_data, data, missing_data_val))
        
    return corrected_data
    
# Fills in the unknown/missing data from existing normal data randomly.
def bootstrap_selection(normal_data, malformed_row, missing_data_val):
    length = len(malformed_row)
    
    corrected_data = []
    
    for index in range(length):
        if malformed_row[index] is "?":
            corrected_data.append(random.choice(normal_data)[index])
        else:
            corrected_data.append(malformed_row[index])
            
    return corrected_data


def shuffle_all(training_data, percent):
    return_data = training_data
    if len(return_data) > 0:
        attribute_count = 0
        for attribute in return_data[0]:
            shuffle_data(return_data, percent, attribute_count)
            attribute_count += 1
    return return_data
    
# Shuffles X% of the data for an attribute specified by row of dataset.
def shuffle_data(training_data, percent, attribute):
    
    shuffling = []
    
    if(percent <= 100):
        num_to_shuffle = int(len(training_data) * percent)
        
        # Will need to pull X% of the rows out of the database at random
        for iter in range(0, num_to_shuffle):
            data_row = random.choice(training_data)
            training_data.remove(data_row)
            
            # Adds the row data to be shuffled.
            shuffling.append(data_row)
        
        # Now we shift all the attribute's in the column specified down one from the randomly generated shuffle list.
        last_attribute = shuffling[-1][attribute]
        temp_attribute = shuffling[0][attribute]
        
        # Sets the first row's attribute equal to the last row's.
        shuffling[0][attribute] = last_attribute
        training_data.append(shuffling.pop(0))
        
        # Shuffles remaining data
        for data_row in shuffling:
            temp = data_row[attribute]
            data_row[attribute] = temp_attribute
            temp_attribute = temp
        
        training_data += shuffling
        # print("Data Shuffled by",(percent*100),"%")
    else:
        print("ERROR: can't shuffle more than the size of the database.")
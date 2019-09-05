from database import database as db

# Loads the file contents into a database object
def process_database_file(file_name):
    file = open(file_name, "r")
    # TODO: Change to use numpy for efficiency's sake?
    data = []
    for set in file:
        # Converts the string line from the file into a set of values.
        data.append(string_to_set(set))
            
    file.close()
    database = db(data)

    return database

# Converts comma seperated strings into a set of values.
def string_to_set(value):
    value = value.strip('\n')
    value_set = value.split(",")
    return value_set

# Either removes data with missing parameters, or extrapolates missing data using bootstraping methodology.
def data_correction(database, parameter_count):
    
    correction_queue = []
    
    # Checks if the data from a specific row has all of the required parameters. If not, pops it from the list into a later processing queue.
    for data in database:
        if len(data) is not parameter_count:
            correction_queue.append(data)
            database.remove(data)
            
    print(correction_queue)

# Deal with missing attributes
    # Remove if 'low' number of missing attributes.
    # Otherwise: Generate a random attribute from a pool of prexisting ones?
        # Set up a queue of lines that need to do this, so we have the pool already fully generated.
            # DOCUMENT THIS CHOICE.
            
# 
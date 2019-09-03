
# Loads the file entirly into memory for processing
def process_database_file(file_name):
    file = open(file_name, "r+")
    # TODO: Change to use numpy for efficiency's sake?
    database = []
    for set in file:
        # TODO: break up set into an actual set of the values, don't leave it as a string!
        database.append(set)
    file.close()
    return database
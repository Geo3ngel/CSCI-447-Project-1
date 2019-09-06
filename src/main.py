""" -------------------------------------------------------------
@file        main.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       The file that runs the program
"""

import process_data

print("Starting...")
db = process_data.process_database_file("../databases/soybean/soybean-small.data")
# db.to_string()
process_data.data_correction(db.get_data(), 36)
print("Finished.")
""" -------------------------------------------------------------
@file        main.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       The file that runs the program
"""

import process_data

print("Starting...")
db = process_data.process_database_file("../databases/soybean/soybean-small.data")
# db.to_string()
normal_data, irregular_data = process_data.data_correction(db.get_data(), 36)
print("Normal Data:\n" + str(normal_data))
print("Irregular Data:\n" + str(irregular_data))
print("Finished.")
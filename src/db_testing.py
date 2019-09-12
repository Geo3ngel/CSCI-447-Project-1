from classifier import add_noise
import os
import process_data
from path_manager import pathManager as pm


# Prepare iris database for testing purposes
full_path = "/Users/admin/Desktop/2019 Fall Semester/Machine Learning/CSCI-447-Project-1/databases/iris/iris.data"
db = process_data.process_database_file(full_path)
add_noise(db, 4)


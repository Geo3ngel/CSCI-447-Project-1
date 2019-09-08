import os
from pathlib import Path

class pathManager:
    
    def __init__(self):
        print("Path manager initializing...")
        
        # Stores the root directory of the project.
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Initializes the folder name for the directory that holds the databases.
        self.databases_dir = "databases"
        
        print("Path manager Initialized!")
        
    def get_databases_dir(self):
        return self.databases_dir
    
    def set_databases_dir(self, folder_name):
        self.databases_dir = folder_name
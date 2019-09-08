import os
from pathlib import Path

class pathManager:
    
    def __init__(self):
        print("Path manager initializing...")
        
        # Stores the root directory of the project.
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Initializes the folder name for the directory that holds the databases.
        self.databases_folder = "databases"
        
        self.update_databases_dir()
        
        print("Path manager Initialized!")
        
    ### DATABASE PATH RELATED:    
    
    def get_ROOT_DIR(self):
        return self.ROOT_DIR
        
    def update_databases_dir(self):
        # Joins the database folder in such a way that is supported on every OS.
        self.databases_dir = os.path.join(self.ROOT_DIR, self.databases_folder)
        
    def get_databases_dir(self):
        return self.databases_dir
    
    def set_databases_folder(self, folder_name):
        self.databases_folder = folder_name
        self.update_databases_dir()
        
    ### FINDING FILES/DIRECTORIES
        
    # Finds files in a specified directory with a specified extension.
    def find_files(dir, ext):
        ext_len = -1*len(ext)
        for (dirpath, dirnames, filenames) in os.walk(dir):
            return filenames    
    
    # Returns folders in a specified directory
    def find_folders(dir):
        folders = []
        for (dirpath, dirnames, filenames) in os.walk(dir):
            folders.extend(dirnames)
            break

        return folders
    
    
    
    ### VALIDATING FILES/DIRECTORIES
    
    # Returns True if the file path entered is valid/non-empty
    def validate_file(self, file_path):
        if file_path is None:
            return False
        elif os.path.exists(file_path):
            return True
        else:
            return False
        
    # Returns True si the directory path entered is valid/non-empty
    def validate_dir(self, dir_path):
        if dir_path is None:
            return False
        elif os.path.isdir(dir_path):
            return True
        else:
            return False
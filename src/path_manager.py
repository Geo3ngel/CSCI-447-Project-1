""" -------------------------------------------------------------
@file        path_manager.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       Contains all functionality related to navigating
             the repository file system
"""

import os
from pathlib import Path

class pathManager:
    
    def __init__(self):
        print("Path manager initializing...")
        
        # Stores the root directory of the project.
        self.ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Initializes the folder name for the directory that holds the databases.
        self.databases_folder = "databases"
        
        # Initialize this to empty
        self.current_selected_folder = ""
        
        print("Path manager Initialized!")
        
    ### DATABASE PATH RELATED:    
    
    def get_ROOT_DIR(self):
        return self.ROOT_DIR
        
    # Returns the entire path of the database collection folder.
    def get_databases_dir(self):
        return os.path.join(self.ROOT_DIR, self.databases_folder)
    
    # Sets the databases folder to the foldername specified, which will then be used to generate the new folder path.
    def set_databases_folder(self, folder_name):
        if self.validate_dir(os.path.join(self.ROOT_DIR, folder_name)):
            self.databases_folder = folder_name
        else:
            print("Please enter a valid database collection directory.")
        
    # Gets the currently selected folder
    def get_current_selected_folder(self):
        return self.current_selected_folder
    
    # Sets the currently selected folder
    def set_current_selected_folder(self, folder_name):
        if self.validate_dir(os.path.join(self.get_databases_dir(), folder_name)):
            self.current_selected_folder = folder_name
        else:
            print("Error: Invalid directory for currently selected folder:", folder_name, "@", os.path.join(self.get_databases_dir(), folder_name))
    
    def get_current_selected_dir(self):
        return os.path.join(self.get_databases_dir(), self.current_selected_folder)
    
    ### FINDING FILES/DIRECTORIES
        
    # Finds files in a specified directory with a specified extension.
    def find_files(self, dir, ext):
        ext_len = len(ext)
        
        files = []
        
        for file in os.listdir(dir):
            if file.endswith(ext):
                files.append(file)
        
        return files
                
    
    # Returns folders in a specified directory
    def find_folders(self, dir):
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
""" -------------------------------------------------------------
@file        database.py
@authors     George Engel, Troy Oster, Dana Parker, Henry Soule
@brief       Object that stores the information of
             each data repository

TODO: Change the brief for data_array in case I'm wrong —Dana
"""

class database:
    """
    @param  data_array  List of pre-processed data from
                        one data repository
    
    FIXME: Modify @param data_array's description 
           in case I'm wrong —Dana
    """
    def __init__(self, data_array):
        print("Database initialized.")
        self.data = data_array
        
    def to_string(self):
        print(self.data)
        
    def get_data(self):
        return self.data
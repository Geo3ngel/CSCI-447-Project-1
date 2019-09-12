""" -------------------------------------------------------------
@file       database.py
@authors    George Engel, Troy Oster, Dana Parker, Henry Soule
@brief      Object that stores the information of
            each data repository for ease of access & manipulation
"""

import random

class database:
    """
    @param  data_array  List of data from one data repository
                        that will be or has been filtered.
    """
    def __init__(self, data_array):
        print("Database initialized.")
        self.data = data_array
        
    def to_string(self):
        print(self.data)
        
    def get_data(self):
        return self.data
    
    def set_data(self, data_array):
        self.data = data_array
    
    # Shuffles X% of the data for an attribute specified by row of dataset.
    def shuffle_data(self, percent, attribute):
        
        shuffling = []
        
        if(percent <= 100):
            num_to_shuffle = int(len(self.data) * percent)
            
            # Will need to pull X% of the rows out of the database at random
            for iter in range(0, num_to_shuffle):
                data_row = random.choice(self.data)
                self.data.remove(data_row)
                
                # Adds the row data to be shuffled.
                shuffling.append(data_row)
            
            # Now we shift all the attribute's in the column specified down one from the randomly generated shuffle list.
            last_attribute = shuffling[-1][attribute]
            temp_attribute = shuffling[0][attribute]
            
            # Sets the first row's attribute equal to the last row's.
            shuffling[0][attribute] = last_attribute
            self.data.append(shuffling.pop(0))
            
            # Shuffles remaining data
            for data_row in shuffling:
                temp = data_row[attribute]
                data_row[attribute] = temp_attribute
                temp_attribute = temp
            
            self.data += shuffling
            print("Data Shuffled by",(percent*100),"%")
        else:
            print("ERROR: can't shuffle more than the size of the database.")
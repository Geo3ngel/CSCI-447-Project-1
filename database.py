

class database:
    
    def __init__(self, data_array):
        print("Database initialized.")
        self.data = data_array
        
    def to_string(self):
        print(self.data)
        
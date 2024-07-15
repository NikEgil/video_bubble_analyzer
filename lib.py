class Mas:
    # конструктор
    def __init__(self,m):
        self.data=[0]*m    

    def __str__(self):
        return str(self.data)
    
    def __repr__(self):
        return repr(self.data)

    def __getitem__(self,key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value
 
    def __delitem__(self, key):
        del self.data[key]

    def get(self):
        return self
    
    def push(self,new_data):
        self.data.extend(new_data)
        del self.data[0:len(new_data)]
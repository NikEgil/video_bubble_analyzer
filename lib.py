# import numpy as np
# import time
# from scipy.ndimage import shift
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
# l=[]*200000
# q=[]
# for i in range(5000):
#     q.append(i)

# st=time.time()
# for i in range(100000):
#     l.append(q)
#     del l[0:len(q)]
# print(time.time()-st)

# st=time.time()
# for i in range(100000):
#     a[:195000]=a[5000:]
#     a[-5000:]=b
# print(time.time()-st)

# st=time.time()
# for i in range(100000):
#     shift(a,5000,b)
# print(time.time()-st)
# m1=np.zeros(200000)
# l=len(q)
# st=time.time()
# for i in range(10000):
#     m1=np.append(m1[l:],q)
# print(time.time()-st)

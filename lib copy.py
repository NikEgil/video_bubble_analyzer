import numpy as np
import time
class colors:
    # конструктор
    def __init__(self,m,n):
        self.R=[[0]*m]
        self.G=[[0]*m]
        self.B=[[0]*m]
       # print("Создание объекта Person",self)
    
    def rou(self):
        for j in range(len(self.data)):
            self.data[j]=j

    def __(self):
        return self.data

    def g(self):
        return self.data
    
    def push(self,chanel,new_data):
        l=len(new_data)
        self.data[n]=np.append(self.data[n][l:],new_data)

    


tt=Mas(1,200000)
l=[]*200000
q=[]
for i in range(5000):
    q.append(i)

st=time.time()
for i in range(10000):
    l.append(q)
    del l[0:5000]
print(time.time()-st)

st=time.time()
for i in range(10000):
    tt.push(0,q)
print(time.time()-st)


m1=np.zeros(200000)
l=len(q)
st=time.time()
for i in range(10000):
    m1=np.append(m1[l:],q)
print(time.time()-st)

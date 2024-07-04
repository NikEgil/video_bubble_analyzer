def array_to_str(arr):
    s=[]
    for i in range(len(arr)):
        s.append(str(arr[i])+'\t')
    return s

q=array_to_str([1,2,50])
print(q)
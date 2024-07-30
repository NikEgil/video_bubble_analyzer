import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

b = pd.DataFrame(columns=["R", "G", "B", "time"])
b.loc[len(b)] = [1, 21, 31, "aaa"]
b.loc[len(b)] = [2, 22, 32, "bbb"]
b.loc[len(b)] = [3, 23, 33, "ccc"]
b.loc[len(b)] = [4, 24, 34, "ddd"]
b.loc[len(b)] = [5, 25, 35, "vvv"]
print(b)
print(b[["R", "G", "B"]].to_numpy() / 255)
# plt.scatter([1, 2, 3], [1, 2, 3], color=[[0, 0.2, 0.5], [1, 0.8, 0.5], [0, 0.2, 0.5]])
# plt.show()
# p = pd.DataFrame(a, columns=["a", "b", "c"])
# print(p)

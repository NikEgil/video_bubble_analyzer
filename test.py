import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageTk
import cv2 as cv2
import time
import lib
from threading import Thread
import imageio.v3 as iio
import os

a=pd.read_table('samples\RGB_detect 1 09.33.13.txt', sep=';')
a=a[380:1120]
R=a['R'].to_numpy()
G=a['G'].to_numpy()
B=a['B'].to_numpy()
Buble=a['is Buble'].to_list()

plt.plot(R,c='tab:red',linestyle='--')
plt.plot(G,c='tab:green',linestyle='--')
plt.plot(B,c='tab:blue',linestyle='--')

l=len(R)
ml=int(l*0.2)
cr=np.average(R[ml:l-ml])
cb=np.average(B[ml:l-ml])
cg=np.average(G[ml:l-ml])


plt.plot(np.linspace(ml,l-ml,l-2*ml),np.ones(l-2*ml)*cr,c='red',lw=2)
plt.plot(np.linspace(ml,l-ml,l-2*ml),np.ones(l-2*ml)*cb,c='blue',lw=2)
plt.plot(np.linspace(ml,l-ml,l-2*ml),np.ones(l-2*ml)*cg,c='green',lw=2)


plt.show()
import tkinter as tk
from tkinter import *
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
from multiprocessing import Process
import cv2 as cv2
import time
import lib
from threading import Thread

import imageio.v3 as iio

# vid = imageio.get_reader('<video0>')

vid = iio.imiter("<video0>")
frame=0
base=[10,10,10,10,10,10]

#(x0,y0,x1,y1)
pos=(152, 207, 248, 303)
pos_rs=list(np.array(pos)/1.5)


root = tk.Tk()
figure1 = plt.Figure(figsize=(6, 5), dpi=100)

ax = figure1.add_subplot(111)
ax.set_ylim(0,255)
fig = FigureCanvasTkAgg(figure1, root)
fig.get_tk_widget().pack(side=tk.LEFT, fill='both')

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()

flag=False

stack=[]
stack_size=300
count=0
st=time.time()
img=0
ct=time.time()


def video_capture():
    global stack
    global frame
    while True:
        frame=next(vid)
        stack.append(frame)
        # count+=1
        # if time.time()-ct>1: 
        time.sleep(0.01)
        #     print(count/dt)
        #     print(count)
        #     ct=time.time()
        #     stack_size=count
        #     count=0
        #     root.event_generate("<<event>>")
        #     stack=[]
        # ms=time.time()-st 
        # if ms<0.01:
        #     ms=10-ms*1000
        #     ms=int(ms)
        #     # print(st, ms)
        # else:
        #     ms=1
    # root.after(1,video_capture)


def main_threads_start():
    Thread(target=video_capture,daemon=True).start()
    Thread(target=upd_can,daemon=True).start()
    Thread(target=upd_graph,daemon=True).start()
    Thread(target=save,daemon=True).start()

    

def upd_can():
    s=0
    time.sleep(3)
    while True:
        if type(frame) != int:
            img1=Image.fromarray(frame.copy())
            ri=img1.resize((1280,720))
            img=ImageTk.PhotoImage(ri)
            # img = ImageTk.PhotoImage(Image.fromarray(frame))
            if s==10:
                canvas.delete('image','sq','text')
                s=0
                # print("canvas was deleted")
            canvas.create_image(0, 0, image=img, anchor="nw",tags='image') 
            canvas.image=img
            canvas.create_rectangle(pos_rs, tags='sq')
            canvas.create_text(20,20,fill='white', font=('16'), text=s,tags='text')
            s+=1

def analize(raznica,chanel1,chanel2):
    _size=len(chanel1)
    _min=raznica-10
    _max=raznica+10
    col=[]
    for i in range(_size):
        if _min<chanel1[i]-chanel2[i]<_max: #and mi2<mas[1][i]-mas[2][i]<ma2:
            col.append(200)
        else:
            col.append(0)
    return col



size=1000
dsize=50
Red=lib.Mas(size)
Green=lib.Mas(size)
Blue=lib.Mas(size)
new_R=[]
new_G=[]
new_B=[]
control=lib.Mas(size)
dm=lib.Mas(dsize)
new=False
def upd_graph():
    global stack
    time.sleep(3)
    global new_B
    global new_G
    global new_R
    global new
    while True:
        if len(stack)>=dsize:
            s1=stack.copy()
            stack.clear()
            for frame in s1:
                new_R.append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],0]))
                new_G.append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],1]))
                new_B.append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],2]))
            control.push(analize(base[3],new_R,new_G))
            # print(new_B)
            Red.push(new_R)
            Green.push(new_G)
            Blue.push(new_B)
            new =True
            ax.clear()
            ax.plot(Red.data, c='tab:red')
            ax.plot(Green.data, c='tab:green')
            ax.plot(Blue.data, c='tab:blue')
            ax.plot(control.data, c='black')
            # ax.text(500,200,stack_size)
            ax.scatter(50,240,s=200,color=(np.average(new_R)/255,np.average(new_G)/255,np.average(new_B)/255))
            ax.set_ylim(0,255)
            fig.draw_idle()
        else:
            time.sleep(0.005)

def save():
    global new
    i=0
    time.sleep(6)
    name='test'+".txt"
    with open(name, "a") as file:
        file.write('n\ttime\tR\tG\tB\n')
        while True:
            if new and working:
                print('da')
                new=False
                for j in range(len(new_B)):
                    file.write(array_to_str([i,time.ctime(),new_R[j],new_G[j],new_B[j]])+'\n')
                    i+=1
                print('save ',i)
            else:
                time.sleep(0.005)
        file.close()

def array_to_str(arr):
    s=''
    for i in range(len(arr)):
        s+=(str(arr[i])+'\t')
    return s
working=False
def on_closing():
    global working
    working=False
    print('close')

def get_base():
    global base
    #R G B
    base=[Red[size-1],Green[size-1],Blue[size-1]]
    #R-G R-B G-B
    base.extend([Red[size-1]-Green[size-1],Red[size-1]-Blue[size-1],Green[size-1]-Blue[size-1]])
    print("base: ", base)

def move(event):
    global pos
    global pos_rs
    global working
    print(event.keysym)
    shift=5
    size=2
    if event.keysym=='b':
        pos=(pos[0]-size,pos[1]-size,pos[2]+size,pos[3]+size)    
    if event.keysym=='m':
        pos=(pos[0]+size,pos[1]+size,pos[2]-size,pos[3]-size)    
    if event.keysym=="Left":
        pos=(pos[0]-shift,pos[1],pos[2]-shift,pos[3])
    if event.keysym=="Right":
        pos=(pos[0]+shift,pos[1],pos[2]+shift,pos[3])
    if event.keysym=="Up":
        pos=(pos[0],pos[1]-shift,pos[2],pos[3]-shift)
    if event.keysym=="Down":
        pos=(pos[0],pos[1]+shift,pos[2],pos[3]+shift) 
    if event.keysym=="space":
        get_base()  
    if event.keysym=="s":
        if working:
            working=False
        else:
            working=True
        print("working=",working)
    print(pos,pos[2]-pos[0])
    pos_rs=list(np.array(pos)/1.5)

#root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<<event>>",upd_graph)
for i in ('<Up>','<Down>','<Left>','<Right>','<m>','<b>','<space>','<s>'):
    root.bind(i,move)
root.after(1,main_threads_start)
root.mainloop()


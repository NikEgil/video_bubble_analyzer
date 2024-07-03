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
from threading import Thread

import imageio.v3 as iio

# vid = imageio.get_reader('<video0>')

vid = iio.imiter("<video0>")
frame=0
base=[10,10,10,10,10,10]

#(x0,y0,x1,y1)
pos=(152, 307, 248, 403)
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

def analize(mas):
    col=[0]*size
    mi=base[3]-10
    ma=base[3]+10
    for i in range(size):
        if i==0:
            print(mas[0][i]-mas[1][i])
        if mi<mas[0][i]-mas[1][i]<ma:
            col[i]=200
    return col

class mas():
    

size=1000
colors=[[0]*size,[0]*size,[0]*size]
control=[0]*size
def upd_graph():
    global stack
    global colors
    time.sleep(3)
    while True:
        if len(stack)>50:
            s1=stack.copy()
            stack.clear()
            stack_size=len(s1)
            # x1=np.arange(stack_size)
            #[y0:y1,x0:x1,chanel]
            for frame in s1:
                colors[0].append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],0]))
                colors[1].append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],1]))
                colors[2].append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],2])) 
            del colors[0][0:stack_size]
            del colors[1][0:stack_size]
            del colors[2][0:stack_size]
            control=analize(colors)
            ax.clear()
            ax.plot(colors[0], c='tab:red')
            ax.plot(colors[1], c='tab:green')
            ax.plot(colors[2], c='tab:blue')
            ax.plot(control, c='black')
            # ax.text(500,200,stack_size)
            ax.scatter(50,240,s=200,color=(colors[0][stack_size]/255,colors[1][stack_size]/255,colors[2][stack_size]/255))
            ax.set_ylim(0,255)
            fig.draw_idle()
        else:
            time.sleep(0.01)



def get_base():
    global base
    #R G B
    base=[colors[0][size-1],colors[1][size-1],colors[2][size-1]]
    #R-G R-B G-B
    base.extend([base[0]-base[1],base[0]-base[2],base[1]-base[2]])
    print("base: ", base)

def move(event):
    global pos
    global pos_rs
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
    print(pos,pos[2]-pos[0])
    pos_rs=list(np.array(pos)/1.5)


root.bind("<<event>>",upd_graph)
for i in ('<Up>','<Down>','<Left>','<Right>','<m>','<b>','<space>'):
    root.bind(i,move)
root.after(1,main_threads_start)

root.mainloop()


import tkinter as tk
from tkinter import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
from PIL import Image, ImageTk
import cv2 as cv2
import time
import lib
from threading import Thread
import imageio.v3 as iio
import os



vid = iio.imiter("<video0>")

base=[181.65289256198346, 186.5805785123967, 98.29338842975207, -4.927685950413235, 83.3595041322314, 88.28719008264463]
#(x0,y0,x1,y1)
pos=(733, 498, 777, 542)
pos_rs=list(np.array(pos)/1.5)



root = tk.Tk()


figure = plt.Figure(figsize=(6, 5), dpi=100)

ax = figure.add_subplot(111)
ax.set_ylim(0,255)
fig = FigureCanvasTkAgg(figure, root)
fig.get_tk_widget().pack(side=tk.LEFT, fill='both')

canvas = tk.Canvas(root, width=1280, height=720)
canvas.pack()


frame=0
stack=[]
img=0


def video_capture():
    global stack
    global frame
    k=1
    while True:
        frame=next(vid)
        stack.append(frame)
        time.sleep(0.01)


def main_threads_start():
    Thread(target=video_capture,daemon=True).start()
    Thread(target=upd_can,daemon=True).start()
    Thread(target=upd_graph,daemon=True).start()
    Thread(target=analyze,daemon=True).start()
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
            # canvas.create_text(20,20,fill='white', font=('16'), text=is_buble[49],tags='text')
            s+=1

gap=15
def buble_check(base,chanel0,chanel1,chanel2):
    if np.abs(np.average(np.subtract(chanel0,base[0])))<gap:
        if np.abs(np.average(np.subtract(chanel1,base[1])))<gap:
            if np.abs(np.average(np.subtract(chanel2,base[2])))<gap:
                return False
            else:  
                return True
        else:  
            return True
    else:  
        return True



size=2000
dsize=25
Red=lib.Mas(size)
Green=lib.Mas(size)
Blue=lib.Mas(size)
new_R=[]
new_G=[]
new_B=[]
control=lib.Mas(size)
is_buble=False
dm=lib.Mas(dsize)
new=False
do_analyze=False
def upd_graph():
    global stack
    time.sleep(1)
    global new_B
    global new_G
    global new_R
    global new
    global is_buble
    global do_analyze
    while True:
        if len(stack)>=dsize:
            s1=stack.copy()
            stack.clear()
            new_R.clear();new_G.clear();new_B.clear()
            for frame in s1:
                new_R.append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],0]))
                new_G.append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],1]))
                new_B.append(np.average(frame[pos[1]:pos[3],pos[0]:pos[2],2]))
            new =True
            do_analyze=True
            Red.push(new_R)
            Green.push(new_G)
            Blue.push(new_B)
            ax.clear()
            ax.plot(Red.data, c='tab:red')
            ax.plot(Green.data, c='tab:green')
            ax.plot(Blue.data, c='tab:blue')
            ax.plot(control.data, c='black')
            ax.scatter(50,240,s=200,color=(np.average(new_R)/255,np.average(new_G)/255,np.average(new_B)/255))
            ax.set_ylim(0,255)
            fig.draw_idle()
        else:
            time.sleep(0.005)




def get_buble_color(r,g,b):
    global seria 
    global do_new_seria
    if len(r)==0:
        return
    _s=int(len(r)*0.2)
    _e=int(len(r)*0.8)
    a_R=np.average(r[_s:_e])
    a_G=np.average(g[_s:_e])
    a_B=np.average(b[_s:_e])
    seria.append([a_R,a_G,a_B,len(r),time.time()])

seria=[]
average_seria=[]
def do_stak():
    global seria
    global average_seria
    print("делаем серию")
    _r,_g,_b=[],[],[]
    for i in range(len(seria)):
        _r.append(seria[i][0])
        _g.append(seria[i][1])
        _b.append(seria[i][2])
    average_seria.append([np.average(_r),np.average(_g),np.average(_b),len(seria)])
    seria.clear()
    print(average_seria)



def analyze():
    global control
    global do_analyze
    global do_new_seria
    c_R=[]
    c_B=[]
    c_G=[]
    collecting=False
    last_buble_time=time.time()
    while True:
        if do_analyze:
            do_analyze=False
            is_buble=buble_check(base,new_R,new_G,new_B)
            if is_buble:
                do_new_seria=True
                collecting=True
                c_R.extend(new_R)
                c_B.extend(new_B)
                c_G.extend(new_G)
                control.push([0]*dsize)
            else:
                control.push([200]*dsize)
                if collecting:
                    collecting=False
                    print(len(c_R),'передано')
                    get_buble_color(c_R,c_G,c_B)
                    c_B.clear();c_R.clear(),c_G.clear()
                    last_buble_time=time.time()
                if time.time()-last_buble_time>15 and do_new_seria==True:
                    print("da")
                    do_stak()
                    save_average_seria()
                    do_new_seria=False
        else:
            time.sleep(0.001)


number_file=1
def save():
    global new
    global number_file
    i=0
    time.sleep(6)
    name_base='samples//RGB_detect '
    name=name_base+time.ctime()[10:19].replace(':','.')
    while True:
        if working:
            with open(name+".txt", "a") as file:
                file.write('n;time;R;G;B;is Buble\n')
                while True:
                    if new:
                        new=False
                        for j in range(len(new_B)):
                            file.write("{0};{1};{2};{3};{4};{5};{6}".format(i,time.ctime()[10:19], new_R[j], new_G[j], new_B[j],is_buble,'\n'))
                            i+=1
                    if i>1000000:
                        file.close()
                        i=0
                        print('saved file ', name)   
                        name=name_base+str(number_file)+time.ctime()[10:19].replace(':','.')
                        break
                    if not working:
                        i=0
                        file.close()
                        print('saved ')   
                        number_file+=1 
                        break
                    time.sleep(0.001)
        if not working:
            name=name_base+str(number_file)+time.ctime()[10:19].replace(':','.')
        time.sleep(0.001)

                    
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
def save_average_seria():
    import pandas as pd
    df=pd.DataFrame(average_seria)
    df.to_excel('seria.xlsx')
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
            print("SAVE")
            working=True
    if event.keysym=="f":
        save_average_seria()
    print(pos,pos[2]-pos[0])
    pos_rs=list(np.array(pos)/1.5)

#root.protocol("WM_DELETE_WINDOW", on_closing)
root.bind("<<event>>",upd_graph)
for i in ('<Up>','<Down>','<Left>','<Right>','<m>','<b>','<space>','<s>','<f>'):
    root.bind(i,move)
root.after(1,main_threads_start)
root.mainloop()


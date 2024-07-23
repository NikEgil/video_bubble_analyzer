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
import pandas as pd


vid = iio.imiter("<video1>")

# base=np.ones([3,3])*150
base = np.array([[220, 220, 222], [210, 210, 212], [230, 230, 232]])
# (x0,y0,x1,y1)
position = (620, 290, 630, 560)
position_resize = list(np.array(position) / 1.5)


root = tk.Tk()

f_left = Frame(root)
f_right = Frame(root)


figure = plt.Figure(figsize=(6, 3), dpi=120)

ax = figure.add_subplot(111)
fig = FigureCanvasTkAgg(figure, f_left)
fig.get_tk_widget().pack(side=tk.TOP)

figure2 = plt.Figure(figsize=(6, 3), dpi=120)
ax2 = figure2.add_subplot(211)
ax3 = figure2.add_subplot(212)
figure2.tight_layout()
fig2 = FigureCanvasTkAgg(figure2, f_left)
fig2.get_tk_widget().pack(side=tk.BOTTOM)


canvas = tk.Canvas(f_right, width=1280, height=720)
canvas.pack()
f_left.pack(side=tk.LEFT)
f_right.pack(side=tk.RIGHT)


frame = 0
frame_stack = []
img = 0


def VideoCapture():
    global frame_stack
    global frame
    k = 1
    while True:
        frame = next(vid)
        frame_stack.append(frame)
        time.sleep(0.01)


def MainThreads():
    Thread(target=VideoCapture, daemon=True).start()
    Thread(target=UpdateCanvas, daemon=True).start()
    Thread(target=UpdateGraph, daemon=True).start()
    Thread(target=UpdateGraphBuble, daemon=True).start()
    Thread(target=Analyzer, daemon=True).start()
    Thread(target=SaveLog, daemon=True).start()


def UpdateCanvas():
    s = 0
    time.sleep(1)
    while True:
        if type(frame) != int:
            img1 = Image.fromarray(frame.copy())
            ri = img1.resize((1280, 720))
            img = ImageTk.PhotoImage(ri)
            # img = ImageTk.PhotoImage(Image.fromarray(frame))
            if s == 10:
                canvas.delete("image", "sq")
                s = 0
                # print("canvas was deleted")
            canvas.create_image(0, 0, image=img, anchor="nw", tags="image")
            canvas.image = img
            canvas.create_rectangle(position_resize, tags="sq")
            # canvas.create_text(20,20,fill='white', font=('16'), text=is_buble[49],tags='text')
            s += 1


gap = 10

size = 400
dsize = 10
Red = lib.Mas(size)
Green = lib.Mas(size)
Blue = lib.Mas(size)
new_R = []
new_G = []
new_B = []
control = lib.Mas(size)
is_buble = np.ones(1)
new = False
do_Analyzer = False
plotSeparator = False


def UpdateGraphBuble():
    global plotSeparator
    buble = 0
    x_buble = 0
    xl = 10
    print("a")
    while True:
        if len(seria) != buble and len(seria) > 0:
            buble = len(seria)
            st = 0
            if buble > 30:
                st = buble - 30
            if buble % 5 == 0:
                for i in range(st, len(seria)):
                    ax2.scatter(
                        i,
                        seria[i][3],
                        color=(seria[i][0] / 255, seria[i][1] / 255, seria[i][2] / 255),
                        s=150,
                    )
                fig2.draw()
        # if plotSeparator:
        #     ax2.plot([x_buble, x_buble], [0, 200], c="black")
        #     plotSeparator = False
        time.sleep(0.001)


def UpdateGraph():
    global frame_stack
    global new_B
    global new_G
    global new_R
    global new
    global is_buble
    global do_Analyzer
    k = 0
    while True:
        if len(frame_stack) >= dsize:
            s1 = frame_stack.copy()
            frame_stack.clear()
            new_R.clear()
            new_G.clear()
            new_B.clear()
            for frame in s1:
                new_R.append(
                    np.average(
                        frame[position[1] : position[3], position[0] : position[2], 0]
                    )
                )
                new_G.append(
                    np.average(
                        frame[position[1] : position[3], position[0] : position[2], 1]
                    )
                )
                new_B.append(
                    np.average(
                        frame[position[1] : position[3], position[0] : position[2], 2]
                    )
                )
            new = True
            do_Analyzer = True
            Red.push(new_R)
            Green.push(new_G)
            Blue.push(new_B)
            k += 1
            if k == 3:
                ax.cla()
                ax.plot(Red.data, c="tab:red")
                ax.plot(Green.data, c="tab:green")
                ax.plot(Blue.data, c="tab:blue")
                ax.plot(control.data, c="black")
                ax.set_title("RGB в окне")
                ax.set_ylim(0, 255)
                fig.draw_idle()
                k = 0
        else:
            time.sleep(0.001)


def BubleCenterColor(r, g, b):
    global seria
    if len(r) == 0:
        return
    _s = int(len(r) * 0.2)
    _e = int(len(r) * 0.8)
    seria = np.append(
        seria,
        [
            np.average(r[_s:_e]),
            np.average(g[_s:_e]),
            np.average(b[_s:_e]),
            len(r),
            time.ctime()[10:19].replace(":", "."),
        ],
    )


def SaveAVGSeria(s):
    average_seria = np.append(
        average_seria,
        [np.average(s[:, 0]), np.average(s[:, 1]), np.average(s[:, 2]), len(s)],
    )
    avg = pd.DataFrame(average_seria, columns=["R", "G", "B", "len"])
    avg.to_excel("AVG Series.xlsx", index=False)
    del avg


# R,G,B,len,time
seria = np.array(0)
average_seria = np.array(0)


def BubbleToSeria():
    global seria
    global average_seria
    print("делаем серию")
    SaveAVGSeria(seria)
    seriaDF = pd.DataFrame(seria, columns=["R", "G", "B", "len", "time"])
    name = "series/seria " + str(len(average_seria)) + ".xlsx"
    seriaDF.to_excel(name, index=False)
    del seriaDF
    seria.clear()


def BubleCheck(base, chanel0, chanel1, chanel2):
    # массивы true если цвет принадлежит калибровке по маслу
    _r = np.logical_and(chanel0 > base[1][0], chanel0 < base[2][0])
    _g = np.logical_and(chanel1 > base[1][1], chanel1 < base[2][1])
    _b = np.logical_and(chanel2 > base[1][2], chanel2 < base[2][2])
    # возвращает наоборот true= капля
    return np.logical_not(np.logical_and(_r, _g, _b))


def Analyzer():
    global control
    global do_Analyzer
    global do_new_seria
    global plotSeparator
    c_R = []
    c_B = []
    c_G = []
    collecting = False
    last_buble_time = time.time()
    kap = 0
    while True:
        if do_Analyzer:
            do_Analyzer = False
            is_buble = BubleCheck(base, new_R, new_G, new_B)
            control.push(is_buble * 200)
            if is_buble.all():
                do_new_seria = True
                collecting = True
                c_R.extend(new_R)
                c_B.extend(new_B)
                c_G.extend(new_G)
            else:
                if collecting:
                    collecting = False
                    print("капля номер ", kap, " длина ", len(c_R))
                    kap += 1
                    BubleCenterColor(c_R, c_G, c_B)
                    c_B.clear()
                    c_R.clear(), c_G.clear()
                    last_buble_time = time.time()
                if time.time() - last_buble_time > 5 and do_new_seria == True:
                    print("da")
                    BubbleToSeria()
                    plotSeparator = True
                    do_new_seria = False
        else:
            time.sleep(0.001)


number_file = 1


def SaveLog():
    global new
    global number_file
    i = 0
    time.sleep(6)
    name_base = "samples//RGB_detect "
    name = name_base + time.ctime()[10:19].replace(":", ".")
    while True:
        if working:
            with open(name + ".txt", "a") as file:
                file.write("n;time;R;G;B;is Buble\n")
                while True:
                    if new:
                        new = False
                        for j in range(len(new_B)):
                            file.write(
                                "{0};{1};{2};{3};{4};{5};{6}".format(
                                    i,
                                    time.ctime()[10:19],
                                    new_R[j],
                                    new_G[j],
                                    new_B[j],
                                    is_buble,
                                    "\n",
                                )
                            )
                            i += 1
                    if i > 1000000:
                        file.close()
                        i = 0
                        print("saved file ", name)
                        name = (
                            name_base
                            + str(number_file)
                            + time.ctime()[10:19].replace(":", ".")
                        )
                        break
                    if not working:
                        i = 0
                        file.close()
                        print("saved ")
                        number_file += 1
                        break
                    time.sleep(0.001)
        if not working:
            name = name_base + str(number_file) + time.ctime()[10:19].replace(":", ".")
        time.sleep(0.001)


working = False
do_new_seria = True


def SetCalibration():
    global base
    # R G B
    base = np.array([Red[size - 1], Green[size - 1], Blue[size - 1]], dtype=int)
    base = [base, base - gap, base + gap]

    print("base: ", base)


def plotaaa():
    ax2.plot([10, 10], [0, 200], c="black")


def move(event):
    global position
    global position_resize
    global working
    print(event.keysym)
    shift = 5
    size = 2
    if event.keysym == "b":
        position = (
            position[0] - size,
            position[1] - size,
            position[2] + size,
            position[3] + size,
        )
    if event.keysym == "m":
        position = (
            position[0] + size,
            position[1] + size,
            position[2] - size,
            position[3] - size,
        )
    if event.keysym == "Left":
        position = (position[0] - shift, position[1], position[2] - shift, position[3])
    if event.keysym == "Right":
        position = (position[0] + shift, position[1], position[2] + shift, position[3])
    if event.keysym == "Up":
        position = (position[0], position[1] - shift, position[2], position[3] - shift)
    if event.keysym == "Down":
        position = (position[0], position[1] + shift, position[2], position[3] + shift)
    if event.keysym == "c":
        SetCalibration()
    if event.keysym == "p":
        plotaaa()
    if event.keysym == "s":
        if working:
            working = False
        else:
            print("SAVE")
            working = True
    if event.keysym == "f":
        BubbleToSeria()
    print(position, position[2] - position[0])
    position_resize = list(np.array(position) / 1.5)


if not os.path.exists(os.path.join("samples")):
    os.makedirs(os.path.join("samples"))


if not os.path.exists(os.path.join("series")):
    os.makedirs(os.path.join("series"))


for i in (
    "<Up>",
    "<Down>",
    "<Left>",
    "<Right>",
    "<m>",
    "<b>",
    "<space>",
    "<s>",
    "<f>",
    "<c>",
    "<p>",
):
    root.bind(i, move)
root.after(1, MainThreads)
root.mainloop()

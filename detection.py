import PredictLetter as pl
import tkinter as tk
from PIL import ImageTk, Image
import cv2
import time


sentence = []

def clearSen():
    if sentence:
        sentence.clear()

def camCheck():
    if cap.isOpened():
        camLab.config(text="Camera Online", fg="white", bg="green")
    else:
        camLab.config(text="Camera Offline", fg="white", bg="red")
    
    return cap.isOpened()


def streamVideo(counter):
    if camCheck():
        _, frame = cap.read()
        if (counter % 30) == 0:
            letter = pl.predict_letter_from_image(frame)
            if letter == 'del':
                if sentence:
                    sentence.pop()
            elif letter == "space":
                sentence.append("_")
            elif letter != 'nothing':
                sentence.append(letter)
            text.configure(text="".join(sentence))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frame = Image.fromarray(frame)
        ftk = ImageTk.PhotoImage(frame)
        detectLab.ftk = ftk
        detectLab.configure(image=ftk)
    counter += 1
    detectLab.after(1, streamVideo, counter)

    

detectWin = tk.Tk()
detectWin.geometry('800x600')
detectWin.title("ASL detector")

camLab = tk.Label(detectWin)
camLab.pack()

text = tk.Label(text="here is the output")
text.pack()

clear = tk.Button(text="clear", command=clearSen )
clear.pack()

detectLab = tk.Label(detectWin)
detectLab.pack()

cap = cv2.VideoCapture(0)

streamVideo(counter=0)

detectWin.mainloop()
import PredictLetter as pl
import tkinter as tk
from PIL import ImageTk, Image
import cv2
import PlanBDesktopApp.mainMenu
import os

from pynput.keyboard import Controller




    





class detection:
    sentence = []

    keyboard = Controller()
    keyboardLetterCheck = False
    
    # def camCheck():
    #     if cap.isOpened():
    #         camLab.config(text="Camera Online", fg="white", bg="green")
    #     else:
    #         camLab.config(text="Camera Offline", fg="white", bg="red")
    #
    #     return cap.isOpened()
    
    def keyboardLetterCheckTrueOrFalse(self):

        if self.keyboardLetterCheck == False:
            self.keyboardLetterCheck = True
        else:
            self.keyboardLetterCheck = False
    
    def clearSen(self):
        if self.sentence:
            self.sentence.clear()

    def streamVideo(self, counter):
        try:
            _, frame = self.cap.read()
            if (counter % 30) == 0:
                letter = pl.predict_letter_from_image(frame)
                if letter == 'del':
                    if self.sentence:
                        self.sentence.pop()
                elif letter == "space":
                    self.sentence.append("_")
                elif letter != 'nothing':
                    self.sentence.append(letter)
                    if (self.keyboardLetterCheck == True):
                        print(letter)
                        self.keyboard.type(letter)

                self.text.configure(text="".join(self.sentence))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = Image.fromarray(frame)
            self.ftk = ImageTk.PhotoImage(frame)
            self.detectLab.ftk = self.ftk
            self.detectLab.configure(image=self.ftk)
            counter += 1
            self.detectLab.after(1, self.streamVideo, counter)
        except:
            current_directory = os.getcwd()
            # Join the current directory with the file name to get the absolute path
            file_path = os.path.join(current_directory, "Black.JPG")
            self.bgImage = Image.open(file_path)  # Open the image using PIL
            self.ftk = ImageTk.PhotoImage(self.bgImage)
    pass

    def __init__(self):
        self.detectWin = tk.Tk()
        self.detectWin.geometry('1000x750')
        self.detectWin.title("ASL detector")
        self.detectWin.configure(bg='#CFDFEF')

        self.detectWinFrame = tk.Frame(self.detectWin, bg='#CFDFEF')

        # camLab = tk.Label(detectWin)
        # camLab.pack()

        self.text = tk.Label(self.detectWinFrame, text="here is the output", bg='#CFDFEF')
        self.text.pack()

        keyboardLetterCheckOutput = tk.Button(self.detectWinFrame, text="Output Keys", command=self.keyboardLetterCheckTrueOrFalse )
        keyboardLetterCheckOutput.pack()

        self.clear = tk.Button(self.detectWinFrame, text="clear", command=self.clearSen)
        self.clear.pack()

        self.mainMenuButton = tk.Button(self.detectWinFrame, text="Main Menu", command=self.menuBtn)
        self.mainMenuButton.pack()

        self.detectLab = tk.Label(self.detectWinFrame, bg='#CFDFEF')
        self.detectLab.pack()
        self.detectWinFrame.grid(row=0, column=0, columnspan=1, sticky='news', pady=10)
        self.detectWinFrame.pack()

        
        # detectLab = tk.Label(detectWin)
        # detectLab.pack()
        
        self.cap = cv2.VideoCapture(0)

        self.streamVideo(counter=0)

        self.detectWin.mainloop()
    pass

    def menuBtn(self):
        self.cap.release()
        self.detectWin.destroy()
        mainMenu = PlanBDesktopApp.mainMenu.MainMenu()
    pass

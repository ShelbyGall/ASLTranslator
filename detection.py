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
        self.detectWin.geometry('1000x500')
        self.detectWin.minsize(1000, 500)
        self.detectWin.maxsize(1000, 500)
        self.detectWin.title("ASL detector")
        self.detectWin.configure(bg='#FF7372')

        self.winChild = tk.Toplevel()
        self.winChild.geometry("500x500")
        self.winChild.title("ASL Help/Guide")
        self.winChild.configure(bg='#FF7372')

        # Get the current working directory
        current_directory = os.getcwd()

        file_pathBG = os.path.join(current_directory, "ASL_Alphabet.jpg")
        self.bgImage = Image.open(file_pathBG)  # Open the image using PIL
        self.bgImage = self.bgImage.resize((475, 475))
        self.bgImage = ImageTk.PhotoImage(self.bgImage)  # Create PhotoImage

        self.image_child = tk.Label(self.winChild, image=self.bgImage)

        self.image_child.pack()

        self.detectWinFrame = tk.Frame(self.detectWin, bg='#FF7372')

        self.text = tk.Label(self.detectWinFrame, text="here is the output", bg='#FF7372', font=('Arial', 24))
        self.text.grid(row=0, column=1, columnspan=1)

        keyboardLetterCheckOutput = tk.Button(self.detectWinFrame, text="Output Keys", command=self.keyboardLetterCheckTrueOrFalse, bg='black', fg='#fffbbb')
        keyboardLetterCheckOutput.grid(row=1, column=2, columnspan=1)

        self.clear = tk.Button(self.detectWinFrame, text="clear", command=self.clearSen, bg='black', fg='#fffbbb')
        self.clear.grid(row=1, column=0, columnspan=1)

        self.mainMenuButton = tk.Button(self.detectWinFrame, text="Main Menu", command=self.menuBtn, bg='black', fg='#fffbbb')
        self.mainMenuButton.grid(row= 1, column= 1, columnspan=1)

        self.detectLab = tk.Label(self.detectWinFrame, bg='#FF7372')
        self.detectLab.grid(row=2, column=0, columnspan=3, sticky='news')

        self.detectWinFrame.pack()

        self.cap = cv2.VideoCapture(0)

        self.streamVideo(counter=0)

        self.detectWin.mainloop()
    pass

    def menuBtn(self):
        self.cap.release()
        self.detectWin.destroy()
        PlanBDesktopApp.mainMenu.MainMenu()
    pass

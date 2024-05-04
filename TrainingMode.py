import PredictLetter as pl
import tkinter as tk
from PIL import ImageTk, Image
import cv2
import PlanBDesktopApp.mainMenu
import os

import random
import pygame
import time



class TrainingMode:
    # sentence = []

    def play_music(self):
        pygame.mixer.music.load("PracticeModeSong.mp3")
        pygame.mixer.music.play(loops=-1)
    pass

    def stop_music(self):
        pygame.mixer.music.stop()
    pass

    def checkMatch(self):
        if self.letterToMatch == self.lastLetter:
            return True
        else:
            return False

    def randomLetterGenerator(self):
            return random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    pass

    def streamVideo(self, counter):
        try:
            if self.startFlag == 0:
                self.letterToMatch = self.randomLetterGenerator()  # controls letter to match
                self.text.configure(text=self.letterToMatch)
                self.startFlag = 1
            countdown = self.end_time - self.start_time
            _, frame = self.cap.read()
            if (counter % 30) == 0: # runs at 30fps
                self.lastLetter = pl.predict_letter_from_image(frame) # controls user prediction
                if countdown >= self.timer:

                    if self.checkMatch() == True:
                        self.score = self.score + 1
                    else:
                        self.strikes = str(self.strikes) + 'X'
                    self.scoreLabel.configure(text=self.score) # edits score
                    self.strikeList.configure(text=self.strikes)

                    if self.score > 10:
                        self.timer = 5

                    self.predictedLetter.configure(text=self.lastLetter) # reveals what the ASL detector thought it was
                    self.letterToMatch = self.randomLetterGenerator()  # gives next letter to match
                    self.text.configure(text=self.letterToMatch)

                    self.start_time = time.time() # reset timer
                    self.end_time = time.time()


            self.timerLabel.configure(text=str(round(countdown, 0)))

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            frame = Image.fromarray(frame)
            frame = frame.resize((529, 290))
            self.ftk = ImageTk.PhotoImage(frame)
            self.detectLab.ftk = self.ftk
            self.detectLab.configure(image=self.ftk)
            counter += 1
            self.detectLab.after(1, self.streamVideo, counter)
            self.end_time = time.time()
            self.endGame()
        except:
            current_directory = os.getcwd()
            # Join the current directory with the file name to get the absolute path
            file_path = os.path.join(current_directory, "Black.JPG")
            self.bgImage = Image.open(file_path)  # Open the image using PIL
            self.ftk = ImageTk.PhotoImage(self.bgImage)

    pass

    def __init__(self):
        self.startFlag = 0
        self.start_time = time.time()
        self.end_time = time.time()
        self.letterToMatch = ''
        self.lastLetter = ''
        self.strikes = ''
        self.score = 0
        self.timer = 10

        self.detectWin = tk.Tk()
        self.detectWin.geometry('1000x700')
        self.detectWin.minsize(1000, 700)
        self.detectWin.maxsize(1000, 700)
        self.detectWin.title("ASL detector")
        self.detectWin.configure(bg='#CFDFEF')

        pygame.init()
        self.play_music()
        # self.detectWinFrame = tk.Frame(self.detectWin, bg='#CFDFEF')

        # Background Canvas
        self.background = tk.Canvas(self.detectWin, width=1000, height=700, highlightthickness=0)  # create the canvas
        self.background.pack(fill="both", expand=True)  # this fills the container and contained space

        # Get the current working directory
        current_directory = os.getcwd()

        # Join the current directory with the file name to get the absolute path
        file_pathBG = os.path.join(current_directory, "PracticeMode.png")
        self.bgImage = Image.open(file_pathBG)  # Open the image using PIL
        self.bgImage = self.bgImage.resize((1000, 700))
        self.bgImage = ImageTk.PhotoImage(self.bgImage)  # Create PhotoImage

        self.background.create_image(0, 0, image=self.bgImage,
                                     anchor="nw")  # this makes/sets the background and allows it to be stretchable

        # self.frame = tk.Frame(self.background, bg="lightblue")
        # self.frame.pack()

#---------------------------------------------------------------------------------------------------------------------

        self.label5 = tk.Label(self.detectWin, text="Timer:", bg='#9AA6B3', font=('Arial', 14))  # prediction label
        self.label5_window = self.background.create_window(886, 270, window=self.label5, anchor="center")
        self.timerLabel = tk.Label(self.detectWin, text="", bg='#9AA6B3', font=('Arial', 24))  # letter predicted
        self.timer_window = self.background.create_window(886, 300, window=self.timerLabel, anchor="center")

        self.label4 = tk.Label(self.detectWin, text="Score:", bg='#9AA6B3', font=('Arial', 24))  # prediction label
        self.label4_window = self.background.create_window(905, 565, window=self.label4, anchor="center")
        self.scoreLabel = tk.Label(self.detectWin, text="", bg='#9AA6B3', font=('Arial', 34))  # letter predicted
        self.score_window = self.background.create_window(905, 630, window=self.scoreLabel, anchor="center")

        self.label3 = tk.Label(self.detectWin, text="Strikes:", bg='#9AA6B3',font=('Arial', 24))  # prediction label
        self.label3_window = self.background.create_window(95, 565, window=self.label3, anchor="center")
        self.strikeList = tk.Label(self.detectWin, text="", bg='#9AA6B3', font=('Arial', 34))  # letter predicted
        self.strikeList_window = self.background.create_window(95, 630, window=self.strikeList, anchor="center")

        self.label2 = tk.Label(self.detectWin, text="Last Predicted\nLetter:", bg='#9AA6B3', font=('Arial', 24))  # prediction label
        self.label2_window = self.background.create_window(885, 40, window=self.label2, anchor="center")
        self.predictedLetter = tk.Label(self.detectWin, text="", bg='#9AA6B3', font=('Arial', 34))  # letter predicted
        self.predictedLetter_window = self.background.create_window(885, 105, window=self.predictedLetter, anchor="center")

        self.label1 = tk.Label(self.detectWin, text="Letter to Copy:", bg='#9AA6B3', font=('Arial', 50)) # label letter to copy
        self.label1_window = self.background.create_window(497, 93, window=self.label1, anchor="center")
        self.text = tk.Label(self.detectWin, text="", bg='#9AA6B3', font=('Arial', 72)) # shows letter to copy
        self.text_window = self.background.create_window(497, 189, window=self.text, anchor="center")

        self.mainMenuButton = tk.Button(self.detectWin, text="Quit", command=self.menuBtn)
        self.mainMenuButton_window = self.background.create_window(98, 58, window=self.mainMenuButton, anchor="center")

        self.detectLab = tk.Label(self.detectWin, bg='#9AA6B3')
        self.detectLab_window = self.background.create_window(497, 428, window=self.detectLab, anchor="center")

        self.cap = cv2.VideoCapture(0)

        self.streamVideo(counter=0)

        # Bind the click event to the canvas
        self.background.bind("<Button-1>", self.button_clicked)

        self.detectWin.mainloop()

    pass



    def button_clicked(self, event):
        x, y = event.x, event.y
        print(f"Mouse clicked at coordinates: ({x}, {y})")

    def menuBtn(self):
        self.cap.release()
        self.stop_music()
        self.detectWin.destroy()
        PlanBDesktopApp.mainMenu.MainMenu()
    pass

    def endGame(self):
        if (self.strikes == 'XXX'):
            self.cap.release()
            self.stop_music()
            self.detectWin.destroy()
            EndGUI(self.score)
    pass
pass

class EndGUI:
    def __init__(self, finalScore):
        self.endGUI = tk.Tk()
        self.endGUI.title("End Game")

        self.end_label = tk.Label(self.endGUI, text="Game Over!", font=("Arial", 24))
        self.end_label.pack(pady=20)

        self.score_label = tk.Label(self.endGUI, text=f"Your Score: {finalScore}", font=("Arial", 16))
        self.score_label.pack()

        self.main_menu_button = tk.Button(self.endGUI, text="Main Menu", command=self.menuBtn)
        self.main_menu_button.pack(pady=10)

        self.endGUI.mainloop()

    def menuBtn(self):
        self.endGUI.destroy()
        PlanBDesktopApp.mainMenu.MainMenu()
    pass

pass
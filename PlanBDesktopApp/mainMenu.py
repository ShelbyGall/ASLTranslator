import tkinter as tk
from PIL import Image, ImageTk

import TrainingMode
import detection
import os

class MainMenu:

    def __init__(self):
        self.menuPage = tk.Tk()
        self.formatWindow()
        self.createWidgets()
        self.formatWidgets()
        self.menuPage.mainloop()
    pass

    def formatWindow(self):
        # self.menuPage.overrideredirect(1)

        # Calculate the screen width and height
        self.menuPage.geometry('1000x500')
        self.menuPage.minsize(1000, 500)
        self.menuPage.maxsize(1000, 500)
        self.menuPage.title('ASL detector')  # set the name of the window

        screen_width = self.menuPage.winfo_screenwidth()
        screen_height = self.menuPage.winfo_screenheight()

        # Set the window size
        window_width = 1000
        window_height = 500

        # Calculate the position to center the window
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        # Set the geometry of the window to center it on the screen
        self.menuPage.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        # Set the window icon (replace 'icon.ico' with your icon file)
        self.menuPage.iconbitmap()
    pass

    def startBtn(self):
        self.menuPage.destroy()
        detection.detection()
    pass

    def trainingModeBtn(self):
        self.menuPage.destroy()
        TrainingMode.TrainingMode()

    def createWidgets(self):
        # Background Canvas

        self.background = tk.Canvas(self.menuPage, width=1000, height=500, highlightthickness=0) # create the canvas
        self.background.pack(fill="both", expand=True) # this fills the container and contained space

        # Get the current working directory
        current_directory = os.getcwd()

        # Join the current directory with the file name to get the absolute path
        file_pathBG = os.path.join(current_directory, "Background.jpg")
        self.bgImage = Image.open(file_pathBG)  # Open the image using PIL
        self.bgImage = self.bgImage.resize((1000, 500))
        self.bgImage = ImageTk.PhotoImage(self.bgImage)  # Create PhotoImage

        self.background.create_image(0, 0, image=self.bgImage, anchor="nw")  # this makes/sets the background and allows it to be stretchable

        # Create a transparent hitbox button
        # Create a hitbox over the image
        self.hitbox1 = self.background.create_rectangle(276, 275, 454, 320, fill="", outline="") # training
        self.hitbox2 = self.background.create_rectangle(538, 275, 713, 320, fill="", outline="") # practice
        self.hitbox3 = self.background.create_rectangle(405, 339, 582, 383, fill="", outline="") # quit

        # Bind the click event to the canvas
        self.background.bind("<Button-1>", self.button_clicked)
    pass

    # def button_clicked(self, event):
    #     x, y = event.x, event.y
    #     print(f"Mouse clicked at coordinates: ({x}, {y})")

    def button_clicked(self, event):
        x, y = event.x, event.y

        if self.background.coords(self.hitbox1)[0] <= x <= self.background.coords(self.hitbox1)[2] and \
            self.background.coords(self.hitbox1)[1] <= y <= self.background.coords(self.hitbox1)[3]:
            print("Training Button Clicked")
            self.startBtn()
        elif self.background.coords(self.hitbox2)[0] <= x <= self.background.coords(self.hitbox2)[2] and \
            self.background.coords(self.hitbox2)[1] <= y <= self.background.coords(self.hitbox2)[3]:
            print("Practice Button Clicked")
            self.trainingModeBtn() # too bade naming convention screwed up.. training is practice
        elif self.background.coords(self.hitbox3)[0] <= x <= self.background.coords(self.hitbox3)[2] and \
            self.background.coords(self.hitbox3)[1] <= y <= self.background.coords(self.hitbox3)[3]:
            print("Quit Button Clicked")
            self.menuPage.destroy()

    def formatWidgets(self):
        print('format')
    pass
pass

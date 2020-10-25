"""
This file hosts the graphical user interface code"""

import tkinter as tk

class Gui:
    """This class is used to "draw" the graphical user interface through which 
    users interact with photonomist.

    |
    """
    def __init__(self):
        """Constructor method
        |
        """
        self.__gui = tk.Tk()
        self.__main_window()

        self.start_gui()
    
    def __main_window(self):
        """
        Specifies the title and dimensions of main window
        """
        self.__gui.title("Photonomist")
        self.__gui.geometry("500x500")
    
    def start_gui(self):
        """
        Starts the graphical user interface
        """
        self.__gui.mainloop()

if __name__ == "__main__":
    Gui()
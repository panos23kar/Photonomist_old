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
        self.__input_path()

        self.__start_gui()
    
    def __main_window(self):
        """
        Specifies the title and dimensions of main window
        """
        self.__gui.title("Photonomist")
        self.__gui.geometry("500x500")
    
    def __start_gui(self):
        """
        Starts the graphical user interface
        """
        self.__gui.mainloop()
    
    def __input_path(self):
        """
        It hosts input label, input path and input button"""

        e1 = tk.Entry(self.__gui)
        e1.insert(0, 'username')
        e1.pack()

# from tkinter import filedialog
# from tkinter import *

# root = Tk()
# root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
# print (root.filename)

if __name__ == "__main__":
    Gui()
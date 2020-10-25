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
        self.__gui.geometry("460x300")
    
    def __start_gui(self):
        """
        Starts the graphical user interface
        """
        self.__gui.mainloop()
    
    def __input_path(self):
        """
        It hosts input label, input path and input button"""

        self.__input_path_label = tk.Label(self.__gui, text="Input path:")
        self.__input_path_label.place(x=20, y=10)

        self.__input_path_entry = tk.Entry(self.__gui)
        self.__input_path_entry.place(x=90, y=12, width= 300)

        self.__input_path_file_explorer_button  = tk.Button(self.__gui, text="...")
        self.__input_path_file_explorer_button.place(x=395, y=10, height=21)
# from tkinter import filedialog
# from tkinter import *

# root = Tk()
# root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
# print (root.filename)

if __name__ == "__main__":
    Gui()
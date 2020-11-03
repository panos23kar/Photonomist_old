"""
This file hosts the graphical user interface code"""

import tkinter as tk
from tkinter import filedialog
from functools import partial
from photonomist.__main__ import input_path_validation, export_path_validation, tidy_photos

class Gui:
    """This class is used to "draw" the graphical user interface through which 
    users interact with photonomist.

    |
    """
    def __init__(self):
        """Constructor method
        |
        """
        self.__widgets = {}
        self.__photos_roots = ""
        self.__gui = tk.Tk()
        self.__main_window()
        self.__user_paths()

        self.__start_gui()
    
    def __main_window(self):
        """Specifies the title and dimensions of main window, and places the run button in the main window.
        |
        """
        self.__gui.title("Photonomist")
        self.__gui.geometry("460x600")

        #Run Button widget
        self.__run_button = tk.Button(self.__gui, text="Run, Forrest, Run!!", command= self.__run_app)
        self.__run_button.place(x=310, y=160, height=21)
    
    def __start_gui(self):
        """
        Starts the graphical user interface
        |
        """
        self.__gui.mainloop()

    def __user_paths(self):
        """It hosts the label, stringvar, entry and file explorer button for the export path
        |
        """

        for mode in (("input", 20, 22),
                     ("export", 100, 102)):
            #Labels widget
            self.__widgets[mode[0] + "_path_label"] = tk.Label(self.__gui, text= mode[0].capitalize() + " path:")
            self.__widgets[mode[0] + "_path_label"].place(x=20, y=mode[1])

            #String variable widget which dynamically changes the value of the Entry widget
            self.__widgets[mode[0] + "_path_value"] = tk.StringVar()

            #Entries widget
            self.__widgets[mode[0] + "_path_entry"] = tk.Entry(self.__gui, textvariable = self.__widgets[mode[0] + "_path_value"])
            self.__widgets[mode[0] + "_path_entry"].place(x=90, y=mode[2], width= 300)

            #Button widget
            self.__widgets[mode[0] + "_path_button"] = tk.Button(self.__gui, text="...", command = partial(self.__file_explorer, mode[0]))
            self.__widgets[mode[0] + "_path_button"].place(x=395, y=mode[1], height=21)


            #String variable widget which dynamically changes in case of invalid path
            self.__widgets[mode[0] + "_invalid_path_value"] = tk.StringVar()

            #Label widget for invalid paths
            self.__inv_input_file_label = tk.Label(self.__gui, textvariable=self.__widgets[mode[0] + "_invalid_path_value"], foreground="red")
            self.__inv_input_file_label.place(x=20, y=mode[1]+27)
    
    def __file_explorer(self, mode):
        self.__widgets[mode+ "_path_button_value"] = filedialog.askdirectory(initialdir = "/",title = "Select file")
        self.__widgets[mode+ "_path_value"].set(self.__widgets[mode+ "_path_button_value"])
    
    def __run_app(self):

        try:
            self.__photos_roots = input_path_validation(self.__widgets["input_path_value"].get())
        except Exception as e:
            self.__widgets["input_invalid_path_value"].set(str(e))
        else:
            self.__widgets["input_invalid_path_value"].set("")


        try:
            export_path_validation(self.__widgets["export_path_value"].get(), self.__widgets["input_path_value"].get(), self.__photos_roots)
        except Exception as e:
            self.__widgets["export_invalid_path_value"].set(str(e))
        else:
            self.__widgets["export_invalid_path_value"].set("")
            #tidy_photos(self.__widgets["export_path_value"].get(), self.__photos_roots)
        
        # var1 = IntVar()
        # Checkbutton(master, text="male", variable=var1).grid(row=1, sticky=W)
        # var2 = IntVar()
        # Checkbutton(master, text="female", variable=var2).grid(row=2, sticky=W)
        
        my_list = [
            "blab",
            "blablabla",
            "blabla",
            "blablablabla",
            "blab",
            "blablabla",
            "blabla",
            "blablablabla",
            "blab",
            "blablabla",
            "blabla",
            "blablablabla",
        ]

        my_dict = {}
        counter = 0
        my_y = 200
        for kati in my_list:
            my_dict[kati+str(counter)] = tk.IntVar()
            tk.Checkbutton(self.__gui, text=kati, variable=counter).place(x=20, y=my_y)
            counter +=1 
            my_y +=25


if __name__ == "__main__":
    Gui()
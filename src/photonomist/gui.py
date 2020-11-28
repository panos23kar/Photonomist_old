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
        self.__run_button.place(x=310, y=200, height=21)
    
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
                     ("export", 150, 152)):
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
            
            if mode[0] == "input":
                #Button widget
                self.__widgets[mode[0] + "find_photos_button"] = tk.Button(self.__gui, text="Find Photos", command= self.__exclude_window)
                self.__widgets[mode[0] + "find_photos_button"].place(x=340, y=mode[1]+50, height=21)
    
    def __validate_input_path(self):
        try:
            self.__photos_roots = input_path_validation(self.__widgets["input_path_value"].get())
        except Exception as e:
            self.__photos_roots = ""
            self.__widgets["input_invalid_path_value"].set(str(e))
        else:
            self.__widgets["input_invalid_path_value"].set("")

    def __file_explorer(self, mode):
        self.__widgets[mode+ "_path_button_value"] = filedialog.askdirectory(initialdir = "/",title = "Select file")
        self.__widgets[mode+ "_path_value"].set(self.__widgets[mode+ "_path_button_value"])
    
    def __run_app(self):
        self.__validate_input_path()
        
        try:
            export_path_validation(self.__widgets["export_path_value"].get(), self.__widgets["input_path_value"].get(), self.__photos_roots)
        except Exception as e:
            self.__widgets["export_invalid_path_value"].set(str(e))
        else:
            self.__widgets["export_invalid_path_value"].set("")
            #tidy_photos(self.__widgets["export_path_value"].get(), self.__photos_roots)

    #------------------------------ Exclude Window-------------------------------------#
    
    def __exclude_window(self):
        try:
            self.__validate_input_path()
            if not self.__photos_roots:
                raise Exception
        except:
            pass
        else:
            self.__exclude_window_layout()
    
    def __exclude_window_layout(self):

        # Exclude window cconfiguration
        self.__found_photos_window = tk.Toplevel(self.__gui)
        self.__found_photos_window.title("Photos Folders")
        ## Exclude window gets the 'full' focus of the app
        self.__found_photos_window.grab_set()

        ##Canvas for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_canvas = tk.Canvas(self.__found_photos_window, borderwidth=0, background="#ffffff")
        self.__excl_w_canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.__excl_w_canvas.pack(side="left", fill="both", expand=True)

        ##Frame for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_frame = tk.Frame(self.__excl_w_canvas, background="grey95", )
        self.__excl_w_frame.bind("<Configure>", lambda event, canvas=self.__excl_w_canvas: self.onFrameConfigure())
        self.__excl_w_canvas.create_window((1,1), window=self.__excl_w_frame, anchor="n")

        ##Scrollbar for Exclude window
        self.__excl_w_scrollbar = tk.Scrollbar(self.__found_photos_window, orient="vertical", command=self.__excl_w_canvas.yview)
        self.__excl_w_scrollbar.pack(side="right", fill="y")
        self.__excl_w_canvas.configure(yscrollcommand=self.__excl_w_scrollbar.set)
        
        #Number of photos Label for Exclude window
        self.__number_of_photos = len(self.__photos_roots.keys())
        self.__widgets["Numb_photos_label"] = tk.Label(self.__excl_w_frame, text="Hmmm!!! I found " + str(self.__number_of_photos) + "photos!!\n\nUncheck the folders that you don't want me to touch!!", anchor="w", justify="left")
        self.__widgets["Numb_photos_label"].pack(anchor="w")


        #Testing
        photos_folders = set(self.__photos_roots.values())

        self.__my_dict_check_var = {}
        self.__my_dict_check_text = {}
        counter = 1

        for kati in photos_folders:
            self.__my_dict_check_var[kati+str(counter)] = tk.IntVar(value=1)
            self.__my_dict_check_text[kati+str(counter)] = tk.Checkbutton(self.__excl_w_frame, text=kati, variable=self.__my_dict_check_var[kati+str(counter)], onvalue = 1,  offvalue = 0)
            self.__my_dict_check_text[kati+str(counter)].pack(anchor="w")
            counter +=1 
            
        self.__exclude_window_button = tk.Button(self.__excl_w_frame, text="Good2Go", command = self.__excluded_paths) #TODO --> Needs to be connected with a function
        self.__exclude_window_button.pack(side="bottom", padx=5, pady=5)
    
    def onFrameConfigure(self):
        '''Reset the scroll region to encompass the inner frame'''
        self.__excl_w_canvas.configure(scrollregion=self.__excl_w_canvas.bbox("all"))
    
    def _on_mousewheel(self, event):
        #TODO --> ....
        """ It listens for mouse's wheel scrolling. 
        https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar"""
        self.__excl_w_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    
    def __excluded_paths(self):
        """Check if i can get the excluded paths form exclude window"""#TODO-->... you might need to change the roots
        for key,_ in self.__my_dict_check_text.items():
            #print("name= ", key, "state= ", self.__my_dict_check_var[key.replace('\\\\','\\')].get())
            if  self.__my_dict_check_var[key.replace('\\\\','\\')].get() == 0:
                print("-"*40)
                for key_two, value in self.__photos_roots.items():
                    
                    if value in key[:len(value)]:
                        print("-"*40)
                        print('value== ', value, 'key==', key)
                        #del self.__photos_roots[key.replace('\\\\','\\')]
                        continue
        print("-"*40)


if __name__ == "__main__":
    Gui()
"""
This file hosts the graphical user interface code"""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from functools import partial
import webbrowser
# Loading Window
from threading import Thread
from PIL import ImageTk
from PIL import Image

from photonomist.__main__ import input_path_validation, export_path_validation, tidy_photos, open_export_folder

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
        self.__menu()
        self.__user_paths()

        self.__start_gui() 
    
    def __main_window(self):
        """Specifies the title and dimensions of main window, and places the run button in the main window.
        |
        """
        self.__gui.title("Photonomist")
        self.__gui.geometry("440x250")

        #Run Button widget
        self.__run_button = tk.Button(self.__gui, text="Run, Forrest, Run!!", command= partial(self.__start_load_w_thread, self.__run_app), state="disabled")
        
        self.__run_button.place(x=310, y=200, height=21)
    
    def __quit(self):
        if messagebox.askyesno("", "Are you sure you want to quit Photonomist?"):
            self.__gui.destroy()
    
    def __menu(self):
        """Menu on the top of the window
        |
        """
        #Main menu
        self.__main_menu = tk.Menu(self.__gui)
        self.__gui.config(menu=self.__main_menu)
        #SubMenu
        #SubMenu File
        self.__sub_menu_file = tk.Menu(self.__main_menu, tearoff=0)
        self.__main_menu.add_cascade(label="File", menu=self.__sub_menu_file, underline=0)
        # separator is here!
        self.__sub_menu_file.add_separator()
        self.__sub_menu_file.add_command(label="Quit", underline=0, command=self.__quit)
        #SubMenu Info
        self.__main_menu.add_command(label="Info...", command=self.__info_app, underline=1)
    
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
                self.__widgets[mode[0] + "find_photos_button"] = tk.Button(self.__gui, text="Find Photos", command= self.__excl_window)
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
        if mode == "input":
            self.__run_button["state"] = "disabled"
    
    def __run_app(self):
        self.__validate_input_path()
        
        try:
            export_path_validation(self.__widgets["export_path_value"].get(), self.__widgets["input_path_value"].get(), self.__photos_roots)
        except Exception as e:
            self.__widgets["export_invalid_path_value"].set(str(e))
        else:
            self.__widgets["export_invalid_path_value"].set("")
            tidy_photos(self.__widgets["export_path_value"].get(), self.__excl_photos_roots)
            open_export_folder(self.__widgets["export_path_value"].get())
            
    #------------------------------ Exclude Window-------------------------------------#
    
    def __excl_window(self):
        try:
            self.__validate_input_path()
            if not self.__photos_roots:
                raise Exception
        except:
            pass
        else:
            # Triggers oading window
            self.__start_load_w_thread(self.__excl_w_layout)
    
    def __excl_w_layout(self):

        # Exclude window cconfiguration
        self.__found_photos_window = tk.Toplevel(self.__gui)
        self.__found_photos_window.title("Photos Folders")
        ## Exclude window gets the 'full' focus of the app
        self.__found_photos_window.grab_set()

        ##Canvas for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_canvas = tk.Canvas(self.__found_photos_window, borderwidth=0, background="#ffffff")
        self.__excl_w_canvas.bind_all("<MouseWheel>", self.__on_mousewheel)
        self.__excl_w_canvas.pack(side="left", fill="both", expand=True)

        ##Frame for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_frame = tk.Frame(self.__excl_w_canvas, background="grey95", )
        self.__excl_w_frame.bind("<Configure>", lambda event, canvas=self.__excl_w_canvas: self.__on_frame_configure())
        self.__excl_w_canvas.create_window((1,1), window=self.__excl_w_frame, anchor="n")

        ##Scrollbar for Exclude window
        self.__excl_w_scrollbar = tk.Scrollbar(self.__found_photos_window, orient="vertical", command=self.__excl_w_canvas.yview)
        self.__excl_w_scrollbar.pack(side="right", fill="y")
        self.__excl_w_canvas.configure(yscrollcommand=self.__excl_w_scrollbar.set)

        self.__excl_w_number_photos()
        self.__excl_w_checkboxes()
        self.__excl_w_resize_canvas()


    def __on_frame_configure(self):
        '''Reset the scroll region to encompass the inner frame'''
        self.__excl_w_canvas.configure(scrollregion=self.__excl_w_canvas.bbox("all"))
    
    def __on_mousewheel(self, event):
        """ It listens for mouse's wheel scrolling. 
        https://stackoverflow.com/questions/17355902/tkinter-binding-mousewheel-to-scrollbar"""
        self.__excl_w_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def __excl_w_number_photos(self):
        #Number of photos Label for Exclude window
        self.__number_of_photos = 0
        for photo_list in self.__photos_roots.values():
            self.__number_of_photos += len(photo_list)
        
        self.__widgets["Numb_photos_label"] = tk.Label(self.__excl_w_frame, text="I found " + str(self.__number_of_photos) + " photos in the folders below!\nUncheck the folders that you don't want me to touch!\n", justify="center")
        self.__widgets["Numb_photos_label"].pack(anchor="center")

    def __excl_w_checkboxes(self):
        self.__photos_folders = set(self.__photos_roots.keys())

        self.__excl_w_checkbox_variables = {}
        self.__excl_w_checkboxes_dict = {}

        for photo_folder in self.__photos_folders:
            self.__excl_w_checkbox_variables[photo_folder] = tk.IntVar(value=1)
            self.__excl_w_checkboxes_dict[photo_folder] = tk.Checkbutton(self.__excl_w_frame, text=photo_folder, variable=self.__excl_w_checkbox_variables[photo_folder], onvalue = 1,  offvalue = 0)
            self.__excl_w_checkboxes_dict[photo_folder].pack(anchor="w")
            
        self.__exclude_window_button = tk.Button(self.__excl_w_frame, text="Good2Go", command = self.__exclude_paths) #TODO --> Needs to be connected with a function
        self.__exclude_window_button.pack(side="bottom", padx=5, pady=5)
    
    def __excl_w_resize_canvas(self):
        self.__excl_w_frame.update()
        self.__excl_w_canvas.configure(width=self.__excl_w_frame.winfo_width())
        self.__excl_w_canvas.configure(height=self.__excl_w_frame.winfo_height())



    def __exclude_paths(self):
        """Check if I can get the excluded paths form exclude window"""
        for key,_ in self.__excl_w_checkboxes_dict.items():
            if  self.__excl_w_checkbox_variables[key.replace('\\\\','\\')].get() == 0:
                if key in self.__photos_roots:
                    del self.__photos_roots[key]
        self.__excl_photos_roots = self.__photos_roots.copy() # I had strange issues when I sent the photos_roots dict without copying
        self.__run_button["state"] = "normal"
        # Close Toplevel window
        self.__found_photos_window.destroy()
        self.__found_photos_window.update()
    
    #------------------------------ Info Window-------------------------------------#

    def __info_app(self):

        # Info window cconfiguration
        self.__info_window = tk.Toplevel(self.__gui)
        self.__info_window.title("Photonomist Info")
        self.__info_window.geometry("640x400")
        ## Exclude window gets the 'full' focus of the app
        self.__info_window.grab_set()

        # Info Windows labels
        self.__info_w_labels = {}
        # Labels widget
        # Aim
        self.__info_w_labels["photonomist_title"] = tk.Label(self.__info_window, text= "Photonomist", font="Helvetica 16 bold italic")
        self.__info_w_labels["photonomist_title"].place(x=10, y=10)

        self.__info_w_labels["aim"] = tk.Label(self.__info_window, justify="left", text="Photonomist aims at helping photo-lovers (or simply photo-owners) with tidying their photos. \n\nGiven a path that contains photos, photonomist will: \n  - extract the dates of your photos, \n  - create 'date' directories \n  - group photos according to their dates", font="Helvetica 10")
        self.__info_w_labels["aim"].place(x=10, y=40)

        # Name
        self.__info_w_labels["name_title"] = tk.Label(self.__info_window, text= "It took its name from the words:", font="Helvetica 11 bold")
        self.__info_w_labels["name_title"].place(x=10, y=170)

        self.__info_w_labels["name"] = tk.Label(self.__info_window, justify="left", text="Photo..   --> Photography (art of captruring the light:: Greek root: (Φως) Φωτογραφία)\n..nomist  --> Taxonomist  (person who groups entities into categories:: Greek root: Ταξινομία ή Ταξινόμηση)", font="Helvetica 10")
        self.__info_w_labels["name"].place(x=10, y=190)

        # Email
        self.__info_w_labels["email"] = tk.Text(self.__info_window, font="Helvetica 10 bold", width=26, height=1)
        self.__info_w_labels["email"].insert(0.1,"photonomist.23@gmail.com")
        self.__info_w_labels["email"].place(x=10, y=245)
        self.__info_w_labels["email"].configure(bg=self.__info_window.cget('bg'), relief="flat")

        self.__info_w_labels["email_goals"] = tk.Label(self.__info_window, justify="left", text="  - ask for extra functionality \n  - report errors \n  - send your endless love", font="Helvetica 10")
        self.__info_w_labels["email_goals"].place(x=10, y=265)

        # Github Link
        self.__info_w_labels["github_link"] = tk.Label(self.__info_window, text="Click me.. ", font="Helvetica 10 bold", fg="blue", cursor="hand2")
        self.__info_w_labels["github_link"].place(x=10, y=339)
        self.__info_w_labels["github_link"].bind("<Button-1>", lambda e: self.__open_url("https://github.com/panos23kar/Photonomist/blob/master/README.rst"))

        self.__info_w_labels["github_link_text"] = tk.Label(self.__info_window, text=" for Motivation, Features and Development Notes. I definitely deserve your time :D !!")
        self.__info_w_labels["github_link_text"].place(x=75, y=340)
   
    def __open_url(self, url):
        webbrowser.open_new(url)
    
    #----------------------- Loading Window -----------------------------

    def __start_load_w_thread(self, func2run):
        self.__load_widnow_thread = Thread(target=func2run)
        self.__load_widnow_thread.start()

        self.__check_thread()
        #self.__loading_window.after(50, self.__check_thread)
    
    def __check_thread(self):

        if not self.__load_widnow_thread.is_alive():
            # Close Toplevel window
            self.__loading_window.destroy()
            self.__loading_window.update()

        else:
            self.__load_w_layout()
            self.__update_load_w = self.__draw_loading_camera().__next__
            self.__load_w_canvas.after(100, self.__update_load_w)            
    
    def __draw_loading_camera(self):
        image = Image.open(self.__filename)
        angle = 0
        #while True:
        while self.__load_widnow_thread.is_alive():
            tkimage = ImageTk.PhotoImage(image.rotate(angle))
            canvas_obj = self.__load_w_canvas.create_image(
                250, 250, image=tkimage)
            self.__loading_window.after(30,self.__update_load_w)
            yield
            self.__load_w_canvas.delete(canvas_obj)
            angle -= 10
            angle %= 360
        
        self.__loading_window.destroy()
        self.__loading_window.update()
    
    def __load_w_layout(self):

        # Na fugei apo edw!!
        self.__filename = r"src\photonomist\static\camera.png"

        # Load window cconfiguration
        self.__loading_window = tk.Toplevel(self.__gui)
        self.__loading_window.title("I'm working on it!!")
        ## Load window gets the 'full' focus of the app
        self.__loading_window.grab_set()

        ##Canvas for Load window (it is need for scrolling (scrollbar) functionality)
        self.__load_w_canvas = tk.Canvas(self.__loading_window,  width=500, height=500)
        self.__load_w_canvas.pack()













if __name__ == "__main__":
    Gui()
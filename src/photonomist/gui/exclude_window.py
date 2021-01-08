import tkinter as tk

class ExcludeWidnow ():
    def __init__(self, main_window):
        self.__gui = main_window

    def __excl_window(self):
        try:
            self.__validate_input_path()
            if not self.__photos_roots:
                raise Exception
        except:
            pass
        else:
            # Triggers loading window
            self.__start_load_w_thread(self.__excl_w_layout)

    def __excl_w_layout(self):

        # Exclude window cconfiguration
        self.__found_photos_window = tk.Toplevel(self.__gui)
        self.__found_photos_window.title("Photos Folders")
        ## Exclude window gets the 'full' focus of the app
        self.__found_photos_window.grab_set()

        ##Canvas for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_canvas = tk.Canvas(self.__found_photos_window, borderwidth=0)#, background="#ffffff"
        self.__excl_w_canvas.bind_all("<MouseWheel>", self.__on_mousewheel)
        self.__excl_w_canvas.pack(side="left", fill="both", expand=True)

        ##Frame for Exclude window (it is need for scrolling (scrollbar) functionality)
        self.__excl_w_frame = tk.Frame(self.__excl_w_canvas, background="grey95", padx=40)
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
        self.__excl_w_checkboxes_arrow_label = {}

        self.__y_coord_link = 54
        for photo_folder in self.__photos_folders:
            self.__excl_w_checkbox_variables[photo_folder] = tk.IntVar(value=1)
            self.__excl_w_checkboxes_dict[photo_folder] = tk.Checkbutton(self.__excl_w_frame, text=photo_folder,  variable=self.__excl_w_checkbox_variables[photo_folder], onvalue = 1,  offvalue = 0)
            self.__excl_w_checkboxes_dict[photo_folder].pack(anchor="w")

            #link close to photo folder paths in order to open the folders in file explorer
            self.__excl_w_checkboxes_arrow_label[photo_folder] = tk.Label(self.__excl_w_frame, text="link", font="Helvetica 8 bold", fg="blue", cursor="hand2")
            self.__excl_w_checkboxes_arrow_label[photo_folder].place(x=self.__calculate_x_coord(len(photo_folder)), y=self.__y_coord_link)
            self.__excl_w_checkboxes_arrow_label[photo_folder].bind("<Button-1>", lambda e, photo_folder=photo_folder:self.__open_folder(photo_folder))
            self.__y_coord_link +=25
        
            
        self.__exclude_window_button = tk.Button(self.__excl_w_frame, text="Good2Go", command = self.__exclude_paths) #TODO --> Needs to be connected with a function
        self.__exclude_window_button.pack(side="bottom", padx=5, pady=5)
    
    def __calculate_x_coord(self, num_of_chars):#TODO-> quick and dirty. chnage it
        if num_of_chars <  20:
            return int(num_of_chars * 6.8 )
        elif num_of_chars <  30:
            return int(num_of_chars * 6.7 )
        elif num_of_chars <  40:
            return int(num_of_chars * 6.25 )
        elif num_of_chars <  50:
            return int(num_of_chars * 6.35 )
        elif num_of_chars <  60:
            return int(num_of_chars * 6.2 )
        elif num_of_chars <  70:
            return int(num_of_chars * 6.15 )
        elif num_of_chars <  80:
            return int(num_of_chars * 6.2 )
        elif num_of_chars <  90:
            return int(num_of_chars * 6.05 )
        elif num_of_chars <  100:
            return int(num_of_chars * 6.05 )
        elif num_of_chars <  110:
            return int(num_of_chars * 6)
        elif num_of_chars <  120:
            return int(num_of_chars * 5.9 )
        elif num_of_chars <  130:
            return int(num_of_chars * 5.85 )
        else:
            return int(num_of_chars * 5.85 )

    def __open_folder(self, photo_folder):
        open_export_folder(photo_folder)


    def __excl_w_resize_canvas(self):

        self.__excl_w_frame.update()


        print("Im here",self.__excl_w_frame.winfo_width())
        #self.__excl_w_frame.configure(width=self.__excl_w_frame.winfo_width() + 30)
        print("Now im here",self.__excl_w_frame.winfo_width())


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
        self.__change_widget_color(self.__widgets["inputfind_photos_button"], "grey95")
        # Close Toplevel window
        self.__found_photos_window.destroy()
        self.__found_photos_window.update()
import tkinter
import tkinter.messagebox
import customtkinter


customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()
        self.title("LearnPath")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")

        # configure title icon
        p1 = tkinter.PhotoImage(file='static/LearnPath Icon.png')
        self.iconphoto(False, p1)

        # center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = int((screen_width / 2) - (App.WIDTH / 2))
        y_cordinate = int((screen_height / 2) - (App.HEIGHT / 2))

        self.geometry("{}x{}+{}+{}".format(App.WIDTH, App.HEIGHT, x_cordinate, y_cordinate))

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=5, pady=0)

        # ============ frame_left ============

        # configure grid layout (1x3)
        self.frame_left.grid_rowconfigure(0,weight=1)
        self.frame_left.grid_rowconfigure(1, weight=8)  # empty row as spacing
        self.frame_left.grid_rowconfigure(2, weight=1)

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Settings",
                                              text_font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=0, column=0, pady=10, padx=10, sticky="n")

        self.switch_1 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_1.grid(row=2, column=0, pady=10, padx=20, sticky="s")

        # ============ frame_right ============

        # configure grid layout (6x3)
        self.frame_right.rowconfigure((0, 1, 2, 3, 4), weight=1)
        self.frame_right.rowconfigure(5, minsize=50)   # empty row with minsize as spacing
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=2)

        # column 0 #
        self.button_1 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Run Init",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                )
        self.button_1.grid(row=0, column=0, pady=10, padx=20)

        self.radio_var = tkinter.IntVar(value=0)

        self.check_box_1 = customtkinter.CTkCheckBox(self.frame_right,
                                                     text="Create",
                                                     command=self.check1)
        self.check_box_1.grid(row=1, column=0, pady=10, padx=20, sticky="w")

        self.check_box_2 = customtkinter.CTkCheckBox(self.frame_right,
                                                     text="Connect Applicants",
                                                     command=self.check2)
        self.check_box_2.grid(row=2, column=0, pady=10, padx=20, sticky="w")

        self.check_box_3 = customtkinter.CTkCheckBox(self.frame_right,
                                                     text="simulate Friends")
        self.check_box_3.grid(row=3, column=0, pady=10, padx=20, sticky="w")

        self.check_box_4 = customtkinter.CTkCheckBox(self.frame_right,
                                                     text="Connect Similars")
        self.check_box_4.grid(row=4, column=0, pady=10, padx=20, sticky="w")

        # column 2 #
        self.button_2 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Run App",
                                                fg_color=("gray75", "gray30"),  # <- custom tuple-color
                                                )
        self.button_2.grid(row=0, column=2, pady=10, padx=20)

        # set default values
        self.switch_1.select()
        # self.check_box_1.configure(state=tkinter.DISABLED, text="CheckBox disabled")
        # self.check_box_2.select()

    # change theme color
    def change_mode(self):
        if self.switch_1.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def check1(self):
        # if check_box_1 is checked create frame_info1 and all its widgets
        if self.check_box_1.get() == 1:
            # configure row 1, col 1 of frame_right
            self.frame_info1 = customtkinter.CTkFrame(master=self.frame_right)
            self.frame_info1.grid(row=1, column=1, columnspan=2, rowspan=1, pady=20, padx=20, sticky="nsew")

            # ============ frame_info1 ============
            # configure grid layout (3x2)
            self.check_box_info1 = customtkinter.CTkCheckBox(self.frame_info1,
                                                             text="Delete Existing")
            self.check_box_info1.grid(row=0, column=0, pady=10, padx=20, sticky="w")

            self.check_box_info2 = customtkinter.CTkCheckBox(self.frame_info1,
                                                             text="Export to File")
            self.check_box_info2.grid(row=1, column=0, pady=10, padx=20, sticky="w")

            self.label_info_1 = customtkinter.CTkLabel(master=self.frame_info1,
                                                       text="Quantity  :",
                                                       height=25,
                                                       justify=tkinter.LEFT)
            self.label_info_1.grid(column=0, row=2, sticky="nwe", padx=1, pady=1)

            self.entry = customtkinter.CTkEntry(master=self.frame_info1,
                                                placeholder_text="Enter number",
                                                width=120,
                                                height=25,
                                                border_width=2,
                                                corner_radius=10)
            self.entry.grid(column=1, row=2, sticky="nwe", padx=1, pady=1)
            self.entry.insert(tkinter.END, '300')
            # create and destroy entry3 in order to make self.entry3.winfo_exists() == 0 work
            self.entry3 = customtkinter.CTkEntry(master=self.frame_info1)
            self.entry3.destroy()
            # if check_box_1 is unchecked destroy frame_info1 and all its widgets
        else:
            self.entry.destroy()
            self.label_info_1.destroy()
            self.check_box_info2.destroy()
            self.check_box_info1.destroy()
            self.frame_info1.destroy()
            # delete entry 3 if it exists
            if self.entry3.winfo_exists() == 1:
                self.entry3.destroy()

    def check2(self):
        # if check_box_2 is checked create frame_info2 and all its widgets
        if self.check_box_2.get() == 1:
            # configure row 2, col 1 of frame_right
            self.frame_info2 = customtkinter.CTkFrame(master=self.frame_right)
            self.frame_info2.grid(row=2, column=1, columnspan=2, rowspan=1, pady=20, padx=20, sticky="nsew")

            # ============ frame_info2 ============

            # configure grid layout (2x2)
            self.check_box_info3 = customtkinter.CTkCheckBox(self.frame_info2,
                                                             text="Delete Existing")
            self.check_box_info3.grid(row=0, column=0, pady=10, padx=20, sticky="w")

            self.label_info_2 = customtkinter.CTkLabel(master=self.frame_info2,
                                                       text="Tries  :",
                                                       height=25,
                                                       justify=tkinter.LEFT)
            self.label_info_2.grid(column=0, row=1, sticky="nwe", padx=1, pady=1)

            self.entry2 = customtkinter.CTkEntry(master=self.frame_info2,
                                                 placeholder_text="Enter number",
                                                 width=120,
                                                 height=25,
                                                 border_width=2,
                                                 corner_radius=10)
            self.entry2.grid(column=1, row=1, sticky="nwe", padx=1, pady=1)
            self.entry2.insert(tkinter.END, '1')
            # create and destroy entry4 in order to make self.entry4.winfo_exists() == 0 work
            self.entry4=customtkinter.CTkEntry(master=self.frame_info2)
            self.entry4.destroy()

            # if check_box_2 is unchecked destroy frame_info2 and all its widgets
        else:
            self.entry2.destroy()
            self.label_info_2.destroy()
            self.check_box_info3.destroy()
            self.frame_info2.destroy()
            # delete entry 4 if it exists
            if self.entry4.winfo_exists() == 1:
                self.entry4.destroy()


    def entry3Fun(self):
        # create entry 3 if it doest exists
        if self.entry3.winfo_exists() == 0:
            self.entry3 = customtkinter.CTkEntry(master=self.frame_info1,
                                                 placeholder_text="Invalid Input",
                                                 width=120,
                                                 height=25,
                                                 border_width=0,
                                                 corner_radius=0
                                                 )
            self.frame_info1.grid_rowconfigure(2, weight=1)
            self.entry3.grid(column=1, row=3, sticky="nwe", padx=1, pady=1)
            self.entry3.configure(state=tkinter.DISABLED, text="CheckBox disabled", text_color="red")

    def entry4Fun(self):
        # create entry 3 if it doest exists
        if self.entry4.winfo_exists() == 0:
            self.entry4 = customtkinter.CTkEntry(master=self.frame_info2,
                                                 placeholder_text="Invalid Input",
                                                 width=120,
                                                 height=25,
                                                 border_width=0,
                                                 corner_radius=0
                                                 )
            self.frame_info2.grid_rowconfigure(2, weight=1)
            self.entry4.grid(column=1, row=2, sticky="nwe", padx=1, pady=1)
            self.entry4.configure(state=tkinter.DISABLED, text="CheckBox disabled", text_color="red")

    def on_closing(self):
        self.destroy()

    def start(self):
        self.mainloop()

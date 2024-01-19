import customtkinter as tk

from custom import CTkXYFrame
from database.Database import Database


class MainScreen(tk.CTk):
    def __init__(self, database: Database):
        super().__init__()
        self.__database = database
        self.__database.create_session()
        self.__messages = []

        self.title('Tutor Talk')
        screen_width = int(self.winfo_screenwidth() / 2)
        screen_height = int(self.winfo_screenheight() / 2)

        self.geometry(f'{screen_width}x{screen_height}')
        self._set_appearance_mode("system")

        self.wm_minsize(int(screen_width / 2), int(screen_height / 2))
        self.resizable(True, True)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.side_bar = tk.CTkFrame(self, width=int(screen_width / 4), corner_radius=0)
        self.side_bar.grid(row=0, column=0, sticky="nsew")
        self.side_bar.grid_rowconfigure(0, weight=1)
        self.side_bar.grid_rowconfigure(1, weight=0)
        self.side_bar.grid_columnconfigure(0, weight=1)
        tk.CTkLabel(self.side_bar, text="No History", width=int(screen_width / 4), corner_radius=0,
                    font=tk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        tk.CTkButton(self.side_bar, text="New Session", corner_radius=0, command=self.create_new_session).grid(row=1,
                                                                                                               column=0,
                                                                                                               sticky="nsew",
                                                                                                               padx=10,
                                                                                                               pady=10)
        self.chat_frame = tk.CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        self.edit_text = None
        self.message_frame = None
        self.create_chat_screen()

    def create_chat_screen(self):
        self.chat_frame = tk.CTkFrame(master=self, corner_radius=0, fg_color="transparent")
        self.chat_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        self.chat_frame.grid_rowconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(1, weight=0)
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.edit_text = tk.CTkEntry(self.chat_frame, corner_radius=0, placeholder_text="Enter your message here")
        self.edit_text.grid(row=1, column=0, sticky="nsew")
        tk.CTkButton(self.chat_frame, text="Enter", corner_radius=0, command=self.add_message).grid(row=1, column=1,
                                                                                                    sticky="nsew")
        self.message_frame = CTkXYFrame(self.chat_frame)
        self.message_frame.grid(row=0, column=0, sticky="nsew", columnspan="2")
        self.add_message()

    def add_message(self):
        label = tk.CTkLabel(self.chat_frame, text="No messages yet")
        if len(self.__messages) == 0 and len(self.edit_text.get()) == 0:
            label.grid(row=0, column=0, sticky="nsew", columnspan="2")
        else:
            for frame in self.chat_frame.winfo_children():  # remove empty label
                if isinstance(frame, tk.CTkLabel):
                    frame.destroy()
            message = self.edit_text.get()
            self.edit_text.delete(0, "end")
            if message == "":
                return
            self.append_message(message)
            for i in range(len(self.__messages)):
                tk.CTkLabel(self.message_frame, text=self.__messages[i], corner_radius=0,
                            font=tk.CTkFont(size=20, weight="bold")).grid(row=i, column=0, sticky="nsew")

    def create_new_session(self):
        self.__database.create_session()
        self.__messages = self.__database.get_last_session().get_messages()
        self.chat_frame.destroy()
        self.create_chat_screen()

    def append_message(self, message):
        self.__database.get_last_session().add_message(message)
        self.__messages = self.__database.get_last_session().get_messages()

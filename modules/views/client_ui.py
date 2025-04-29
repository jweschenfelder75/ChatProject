import threading
from threading import Thread
from tkinter import *
from tkinter import messagebox
from modules.chat_client import ChatClient
from modules.logging import FileLogger
from modules.utils import Utils

"""
Tkinter GUI for the Socket Client.
"""


class ClientUI:
    def __init__(self, ip: str, port: int, /):
        """
        Constructor of the class ClientUI.
        IP Address and Port must be the same as the of the Socket Server.

        Args:
            ip (str): IP Address of the Socket Server (where it should be connected to)
            port (int): Port of the Socket Server (where it should be connected to)
        """
        self.__log = FileLogger(ClientUI.__name__)
        self.__client = ChatClient(ip, port)
        self.__stop_event = threading.Event()
        self.__utils = Utils()
        self.__window = None
        self.__name_input = None
        self.__name_confirm_button = None
        self.__chat_log = None
        self.__message_input = None
        self.__send_button = None
        self.__client.connect()
        self.__log.debug("Start Client UI...")
        self.initialize()

    def send(self):
        """
        Sends the entered username and text message via the Socket Client to the Socket Server.
        """
        username = self.__name_input.get()
        message = self.__message_input.get()
        rec_message = self.__client.send(username, message)
        self.print_message(rec_message)
        if message == "[exit]":  # Not really needed at the moment, can be used for client status later
            self.on_close()
        else:
            self.__message_input.delete(0, END)

    def print_message(self, message: str, /):
        """
        Replaces some emojis in a given text and appends the result in the Chat Log window.

        Args:
            message (str): Text message
        """
        message = self.replace_emojis(message)
        self.__chat_log.configure(state=NORMAL)
        self.__chat_log.insert(END, message)
        self.__chat_log.see(END)
        self.__chat_log.configure(state=DISABLED)
        self.__message_input.focus_set()

    def loop_receive(self):
        """
        Listens for new incoming messages from the Socket Server via the Socket Client
        """
        while not self.__stop_event.is_set():
            try:
                result = self.__client.receive()
                if result:
                    if result.success:
                        self.print_message(result.text)
            except Exception as e:
                self.__log.error(f"Encountered error: {e.args}")
                break

    def lock_username(self):
        """
        Disables the username input field after the user has entered a valid username.
        Enables chat functionality.
        """
        username = self.__name_input.get()
        max_len = self.__utils.get_user_header_size()
        if username and username.isprintable() and 0 < len(username.strip()) <= max_len:
            self.__message_input.configure(state=NORMAL)
            self.__send_button.configure(state=NORMAL)
            self.__name_input.configure(state=DISABLED)
            self.__name_confirm_button.configure(state=DISABLED)
            self.__message_input.focus_set()
        else:
            msg = f"Please enter a user name which is between 1 and {max_len} characters long!"
            messagebox.showinfo("Error", msg)

    def on_close(self):
        """
        Shows a MessageBox which asks the user if s(he) really intends to exit/close the Client.
        If Yes, it will shut down the Client Socket gracefully.
        """
        if messagebox.askokcancel("Exit", "Do you really want to exit the chat?"):
            self.__log.debug("Close Client UI...")
            self.__stop_event.set()
            self.__client.disconnect()
            self.__window.destroy()

    def initialize(self):
        """
        Configures the GUI components for the Tkinter GUI.
        """
        title_text = "Chat program"
        self.__window = Tk(className=title_text)
        self.__window.title(title_text)
        self.__window.configure(bg="ghostwhite")
        self.__window.resizable(False, False)

        name_label = Label(self.__window, text="Name", anchor="e", bg="ghostwhite")
        name_label.grid(row=0, column=0, sticky="e")

        self.__name_input = Entry(self.__window, width=100, bg="ghostwhite", disabledbackground="lavender")
        self.__name_input.grid(row=0, column=1)
        self.__name_input.focus_set()

        self.__name_confirm_button = Button(self.__window, width=20, text="Confirm", bg="ghostwhite",
                                     command=self.lock_username)
        self.__name_confirm_button.grid(row=0, column=2)

        self.__chat_log = Text(self.__window, width=100, height=20, bg="lightyellow", state=DISABLED)
        self.__chat_log.grid(row=1, column=0, columnspan=3)

        message_label = Label(self.__window, text="Message", anchor="e", bg="ghostwhite")
        message_label.grid(row=2, column=0, sticky="e")

        self.__message_input = Entry(self.__window, width=100, bg="ghostwhite", disabledbackground="lavender",
                                     state=DISABLED)
        self.__message_input.grid(row=2, column=1)

        self.__send_button = Button(self.__window, width=20, text="Send", bg="ghostwhite", command=self.send,
                                    state=DISABLED)
        self.__send_button.grid(row=2, column=2)

        exit_button = Button(self.__window, width=20, text="Exit", bg="ghostwhite", command=self.on_close)
        exit_button.grid(row=3, column=2)

        receive_thread = Thread(target=self.loop_receive, daemon=True)
        receive_thread.start()

        self.__window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.__window.mainloop()

    @staticmethod
    def replace_emojis(message: str, /) -> str:
        """
        Replaces some emojis in a given text message

        Args:
            message (str): Text message

        Returns:
            str: Message with replaces emojis
        """
        emoji_map = {
            ":)": chr(0x1F642),
            ":-)": chr(0x1F642),
            ":(": chr(0x1F641),
            ":-(": chr(0x1F641),
            ";)": chr(0x1F609),
            ";-)": chr(0x1F609),
            ":D": chr(0x1F604),
            "<3": chr(0x2764),
            ":P": chr(0x1F61B)
        }
        for shortcut, emoji in emoji_map.items():
            message = message.replace(shortcut, emoji)
        return message

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
        self.log = FileLogger(ClientUI.__name__)
        self.client = ChatClient(ip, port)
        self.stop_event = threading.Event()
        self.utils = Utils()
        self.window = None
        self.name_input = None
        self.to_input = None
        self.chat_log = None
        self.message_input = None
        self.send_button = None
        self.client.connect()
        self.initialize()
        self.log.debug("Start Client UI...")

    def send(self):
        """
        Sends the entered username and text message via the Socket Client to the Socket Server.
        """
        username = self.name_input.get()
        message = self.message_input.get()
        rec_message = self.client.send(username, message)
        self.print_message(rec_message)
        if message == "[exit]":  # Not really needed at the moment, can be used for client status later
            self.on_close()
        else:
            self.message_input.delete(0, END)

    def print_message(self, message: str, /):
        """
        Appends a given text message in the Chat Log window.

        Args:
            message (str): Text message
        """
        self.chat_log.configure(state=NORMAL)
        self.chat_log.insert(END, message)
        self.chat_log.configure(state=DISABLED)

    def loop_receive(self):
        """
        Listens for new incoming messages from the Socket Server via the Socket Client
        """
        while not self.stop_event.is_set():
            try:
                result = self.client.receive()
                if result:
                    if result.success:
                        self.print_message(result.text)
            except Exception as e:
                self.log.error(f"Encountered error: {e.args}")
                break

    def lock_username(self):
        """
        Disables the username input field after the user has entered a valid username.
        Enables chat functionality.
        """
        username = self.name_input.get()
        max_len = self.utils.get_user_header_size()
        if username and username.isprintable() and 0 < len(username.strip()) <= max_len:
            self.message_input.configure(state=NORMAL)
            self.send_button.configure(state=NORMAL)
            self.name_input.configure(state=DISABLED)
        else:
            msg = f"Please enter a user name which is between 1 and {max_len} characters long!"
            messagebox.showinfo("Error", msg)

    def on_close(self):
        """
        Shows a MessageBox which asks the user if s(he) really intends to exit/close the Client.
        If Yes, it will shut down the Client Socket gracefully.
        """
        if messagebox.askokcancel("Exit", "Do you really want to exit the chat?"):
            self.log.debug("Close Client UI...")
            self.stop_event.set()
            self.client.disconnect()
            self.window.destroy()

    def initialize(self):
        """
        Configures the GUI components for the Tkinter GUI.
        """
        title_text = "Chat program"
        self.window = Tk(className=title_text)
        self.window.title(title_text)

        name_label = Label(self.window, text="Name", anchor="e")
        name_label.grid(row=0, column=0, sticky="e")

        self.name_input = Entry(self.window, width=100)
        self.name_input.grid(row=0, column=1)
        self.name_input.focus_set()

        name_confirm_button = Button(self.window, width=20, text="Confirm", bg="white", command=self.lock_username)
        name_confirm_button.grid(row=0, column=2)

        self.chat_log = Text(self.window, width=100, height=20, bg="lightyellow", state=DISABLED)
        self.chat_log.grid(row=1, column=0, columnspan=3)

        message_label = Label(self.window, text="Message", anchor="e")
        message_label.grid(row=2, column=0, sticky="e")

        self.message_input = Entry(self.window, width=100, state=DISABLED)
        self.message_input.grid(row=2, column=1)

        self.send_button = Button(self.window, width=20, text="Send", bg="white", command=self.send, state=DISABLED)
        self.send_button.grid(row=2, column=2)

        exit_button = Button(self.window, width=20, text="Exit", bg="white", command=self.on_close)
        exit_button.grid(row=3, column=2)

        receive_thread = Thread(target=self.loop_receive, daemon=True)
        receive_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.window.mainloop()

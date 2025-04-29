import threading
from threading import Thread
from tkinter import *
from tkinter import messagebox
from modules.chat_client import ChatClient
from modules.logging import FileLogger


class ClientUI:
    def __init__(self, ip: str, port: int, /):
        self.log = FileLogger(ClientUI.__name__)
        self.client = ChatClient(ip, port)
        self.stop_event = threading.Event()
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
        username = self.name_input.get()
        message = self.message_input.get()
        rec_message = self.client.send(username, message)
        self.print_message(rec_message)
        if message == "[exit]":
            self.on_close()
        else:
            self.message_input.delete(0, END)

    def print_message(self, message):
        self.chat_log.configure(state=NORMAL)
        self.chat_log.insert(END, message)
        self.chat_log.configure(state=DISABLED)

    def loop_receive(self):
        while not self.stop_event.is_set():
            try:
                result = self.client.receive()
                if result:
                    if result.success:
                        self.print_message(result.text)
                    else:
                        self.on_close()
            except Exception as e:
                self.log.error(f"Encountered error: {e.args}")
                break

    def lock_username(self):
        if self.name_input.get():
            self.message_input.configure(state=NORMAL)
            self.send_button.configure(state=NORMAL)
            self.name_input.configure(state=DISABLED)
        else:
            messagebox.showinfo("Error", "Please enter a user name!")

    def on_close(self):
        self.log.debug("Close Client UI...")
        self.stop_event.set()
        self.client.disconnect()
        self.window.destroy()

    def initialize(self):
        self.window = Tk(className="Chat program")

        name_label = Label(self.window, text="Name", anchor="e")
        name_label.grid(row=0, column=0, sticky="e")

        self.name_input = Entry(self.window, width=100)
        self.name_input.grid(row=0, column=1)
        self.name_input.focus_set()

        name_confirm_button = Button(self.window, width=20, text="Confirm", bg="white", command=self.lock_username)
        name_confirm_button.grid(row=0, column=2)

        to_label = Label(self.window, text="To", anchor="e")
        to_label.grid(row=1, column=0, sticky="e")

        self.to_input = Entry(self.window, width=125)
        self.to_input.grid(row=1, column=1, columnspan=2)

        self.chat_log = Text(self.window, width=100, height=20, bg="lightyellow", state=DISABLED)
        self.chat_log.grid(row=2, column=0, columnspan=3)

        message_label = Label(self.window, text="Message", anchor="e")
        message_label.grid(row=3, column=0, sticky="e")

        self.message_input = Entry(self.window, width=100, state=DISABLED)
        self.message_input.grid(row=3, column=1)

        self.send_button = Button(self.window, width=20, text="Send", bg="white", command=self.send, state=DISABLED)
        self.send_button.grid(row=3, column=2)

        exit_button = Button(self.window, width=20, text="Exit", bg="white", command=self.on_close)
        exit_button.grid(row=4, column=2)

        receive_thread = Thread(target=self.loop_receive, daemon=True)
        receive_thread.start()

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.window.mainloop()

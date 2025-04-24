import sys
from threading import Thread
from tkinter import *
from tkinter import messagebox
from modules.chat_client import ChatClient


class ClientUI:
    def __init__(self, ip: str, port: int, /):
        self.client = ChatClient(ip, port)
        self.name_input = None
        self.chat_log = None
        self.send_button = None
        self.message_input = None
        self.client.connect()
        self.initialize()

    def send(self):
        username = self.name_input.get()
        message = self.message_input.get()
        rec_message = self.client.send(username, message)
        self.print_message(rec_message)
        if message == '[exit]':
            sys.exit()
        else:
            self.message_input.delete(0, END)

    def print_message(self, message):
        self.chat_log.configure(state=NORMAL)
        self.chat_log.insert(END, message)
        self.chat_log.configure(state=DISABLED)

    def loop_receive(self):
        while True:
            message = self.client.receive()
            if message:
                self.print_message(message)

    def lock_username(self):
        if self.name_input.get():
            self.message_input.configure(state=NORMAL)
            self.send_button.configure(state=NORMAL)
            self.name_input.configure(state=DISABLED)
        else:
            messagebox.showinfo('Error', 'Please enter a user name!')

    def initialize(self):
        window = Tk(className='Chat program')
        name_label = Label(window, text='Name')
        name_label.grid(row=0, column=0)

        self.name_input = Entry(window, width=100)
        self.name_input.grid(row=0, column=1)

        name_confirm_button = Button(window, width=20, text='Confirm', bg='white', command=self.lock_username)
        name_confirm_button.grid(row=0, column=2)

        self.chat_log = Text(window, width=100, height=20, state=DISABLED)
        self.chat_log.grid(row=1, column=0, columnspan=3)

        message_label = Label(window, text='Message')
        message_label.grid(row=2, column=0)

        self.message_input = Entry(window, width=100, state=DISABLED)
        self.message_input.grid(row=2, column=1)

        self.send_button = Button(window, width=20, text='Send', bg='white', command=self.send, state=DISABLED)
        self.send_button.grid(row=2, column=2)

        receive_thread = Thread(target=self.loop_receive)
        receive_thread.start()

        window.mainloop()

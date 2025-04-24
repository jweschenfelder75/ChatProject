import socket
import errno
import sys
from threading import Thread
from modules.utils.utils import Utils
from tkinter import *
from tkinter import messagebox

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-3/


class ChatClient:
    def __init__(self, ip: str, port: int, /):
        self.utils = Utils()
        self.ip = ip
        self.port = port
        self.client_socket = None
        self.name_input = None
        self.chat_log = None
        self.send_button = None
        self.message_input = None

    def send(self):
        username = self.name_input.get()
        message = self.message_input.get()
        if message == '[exit]':
            message = self.utils.format_message(username, 'Signing out')
            self.client_socket.send(message.encode('utf-8'))
            self.print_message('\nSigned out')
            self.client_socket.close()
            sys.exit()
        elif message:
            self.print_message(f'\n{username} > {message}')
            formatted_message = self.utils.format_message(username, message).encode('utf-8')
            self.client_socket.send(formatted_message)
            self.message_input.delete(0, END)

    def receive(self):
        try:
            message_size = self.client_socket.recv(self.utils.LENGTH_HEADER_SIZE)
            if message_size:
                message_size = int(message_size.decode('utf-8').strip())
                sender = self.client_socket.recv(self.utils.USER_HEADER_SIZE).decode('utf-8').strip()
                message = self.client_socket.recv(message_size).decode('utf-8')
                self.print_message(f'\n{sender} > {message}')

        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Encountered error while reading', e)
                self.client_socket.close()
                sys.exit()
        except Exception as e:
            print('Encountered error', e)
            self.client_socket.close()
            sys.exit()

    def print_message(self, message):
        self.chat_log.configure(state=NORMAL)
        self.chat_log.insert(END, message)
        self.chat_log.configure(state=DISABLED)

    def loop_receive(self):
        while True:
            self.receive()

    def lock_username(self):
        if self.name_input.get():
            self.message_input.configure(state=NORMAL)
            self.send_button.configure(state=NORMAL)
            self.name_input.configure(state=DISABLED)
        else:
            messagebox.showinfo('Error', 'Please enter a user name!')

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(False)

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

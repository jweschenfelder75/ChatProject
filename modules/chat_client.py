import socket
import errno
import sys
from modules.utils.utils import Utils

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-3/


class ChatClient:
    def __init__(self, ip: str, port: int, /):
        self.utils = Utils()
        self.ip = ip
        self.port = port
        self.client_socket = None

    def send(self, username: str, message: str, /) -> str:
        if message == '[exit]':
            message = self.utils.format_message(username, 'Signing out')
            self.client_socket.send(message.encode('utf-8'))
            self.client_socket.close()
            return '\nSigned out'
        elif message:
            formatted_message = self.utils.format_message(username, message).encode('utf-8')
            self.client_socket.send(formatted_message)
            return f'\n{username} > {message}'

    def receive(self) -> str:
        try:
            message_size = self.client_socket.recv(self.utils.LENGTH_HEADER_SIZE)
            if message_size:
                message_size = int(message_size.decode('utf-8').strip())
                sender = self.client_socket.recv(self.utils.USER_HEADER_SIZE).decode('utf-8').strip()
                message = self.client_socket.recv(message_size).decode('utf-8')
                return f'\n{sender} > {message}'
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                print('Encountered error while reading', e)
                self.client_socket.close()
                sys.exit()
        except Exception as e:
            print('Encountered error', e)
            self.client_socket.close()
            sys.exit()

    def connect(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.ip, self.port))
        self.client_socket.setblocking(False)

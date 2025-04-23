import socket

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-1/


class ChatClient:
    def __init__(self, port: int, /):
        self.port = port

    def connect(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((socket.gethostname(), self.port))
        print(f'Connected on {socket.gethostname()}:{self.port}')

        while True:
            message = client_socket.recv(512)
            if message:
                print(message.decode('utf-8'))

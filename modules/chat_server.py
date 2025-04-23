import socket

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-1/


class ChatServer:
    def __init__(self, port):
        self.port = port

    def connect(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((socket.gethostname(), self.port))
        server_socket.listen(5)
        print(f'Listening on {socket.gethostname()}:{self.port}')

        while True:
            client_socket, client_address = server_socket.accept()
            print(f'Established connection to {client_address[0]}:{client_address[1]}')
            client_socket.send(bytes('Hello there', 'utf-8'))

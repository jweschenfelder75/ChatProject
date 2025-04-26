import socket
import select
from modules.utils import Utils
from modules.views import ServerUI

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-3/


class ChatServer:
    def __init__(self, ip: str, port: int, /):
        self.utils = Utils()
        self.ip = ip
        self.port = port
        self.all_sockets = None
        self.server_socket = None
        self.client_socket = None
        print(ServerUI())

    def receive(self, client_socket: socket.socket, /) -> str | None:
        size_header = client_socket.recv(self.utils.LENGTH_HEADER_SIZE)
        if not size_header:
            return None
        size_header = size_header.decode("utf-8")
        message_size = int(size_header.strip())
        user_header = client_socket.recv(self.utils.USER_HEADER_SIZE).decode("utf-8")
        user = user_header.strip()
        message = client_socket.recv(message_size).decode("utf-8")
        print(f"{user} > {message}")
        return f"{size_header}{user_header}{message}"

    def broadcast(self, sender: socket.socket, message: str, /):
        for item_socket in self.all_sockets:
            if item_socket != sender and item_socket != self.server_socket:
                item_socket.send(message.encode("utf-8"))

    def connect(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(10)
        print(f"Listening on {self.ip}:{self.port}")
        self.all_sockets = [self.server_socket]
        self.listen()

    def listen(self):
        client_socket = None
        while True:
            read_sockets, _, error_sockets = select.select(self.all_sockets, [], self.all_sockets)
            for item_socket in read_sockets:
                if item_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    self.all_sockets.append(client_socket)
                    print(f"Established connection to {client_address[0]}:{client_address[1]}")
                else:
                    try:
                        message = self.receive(item_socket)
                        if not message:
                            client_socket_name = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
                            print(f"{client_socket_name} closed the connection")
                            self.all_sockets.remove(item_socket)
                            continue
                        self.broadcast(item_socket, message)
                    except ConnectionResetError as e:
                        self.all_sockets.remove(item_socket)
                        print("Client forcefully closed the connection", e)

            for error_socket in error_sockets:
                self.all_sockets.remove(error_socket)

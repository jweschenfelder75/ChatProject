import socket
import select
from modules.utils import Utils
from modules.views import ServerUI
from modules.logging import FileLogger
from modules.objects.clientpool import ClientPool

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-3/


class ChatServer:
    def __init__(self, ip: str, port: int, /):
        self.log = FileLogger(ChatServer.__name__)
        self.clientpool = ClientPool([])
        self.utils = Utils()
        self.ip = ip
        self.port = port
        self.all_sockets = None
        self.server_socket = None
        self.client_socket = None
        print(ServerUI())
        self.connect()

    def receive(self, client_socket: socket.socket, /) -> str | None:
        size_header = client_socket.recv(self.utils.get_length_header_size())
        if not size_header:
            return None
        size_header = size_header.decode("utf-8")
        message_size = int(size_header.strip())
        user_header = client_socket.recv(self.utils.get_user_header_size()).decode("utf-8")
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
        self.log.debug("Start ChatServer...")
        self.log.debug(f"Listening on {self.ip}:{self.port}")
        print(f"Listening on {self.ip}:{self.port}")
        self.all_sockets = [self.server_socket]  # TODO -> clientpool
        self.clientpool.add(self.port, self.server_socket, "[ALL]")
        self.listen()

    def listen(self):
        client_socket = None
        while True:
            read_sockets, _, error_sockets = select.select(self.all_sockets, [], self.all_sockets)
            for item_socket in read_sockets:
                if item_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    self.all_sockets.append(client_socket)  # TODO -> clientpool
                    self.clientpool.add(int(client_address[1]), self.client_socket, "[unnamed]")
                    client_address_name = f"{client_address[0]}:{client_address[1]}"
                    self.log.debug(f"Established connection to {client_address_name}")
                    print(f"Established connection to {client_address[0]}:{client_address[1]}")
                else:
                    try:
                        message = self.receive(item_socket)
                        if not message:
                            client_socket_name = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
                            self.log.debug(f"{client_socket_name} closed the connection")
                            print(f"{client_socket_name} closed the connection")
                            self.all_sockets.remove(item_socket)  # TODO -> clientpool
                            self.clientpool.remove(item_socket)
                            continue
                        if "[list]" in message:
                            self.send_client_list(item_socket)
                        else:
                            self.broadcast(item_socket, message)
                    except ConnectionResetError as e:
                        self.all_sockets.remove(item_socket)  # TODO -> clientpool
                        self.clientpool.remove(item_socket)
                        self.log.error(f"Client forcefully closed the connection, {e.args}")
                        print("Client forcefully closed the connection", e)

            for error_socket in error_sockets:
                self.all_sockets.remove(error_socket)  # TODO -> clientpool
                self.clientpool.remove(error_socket)

    def send_client_list(self, requester_socket: socket.socket):
        user_list = []
        for client in self.clientpool.get_list:
            if client:
                try:
                    user_list.append(f"{client.username}")
                except Exception:
                    continue

        message = "[Connected Users]: " + ", ".join(user_list)
        requester_socket.send(message.encode("utf-8"))

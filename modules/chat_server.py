import socket
import select
from modules.utils import Utils
from modules.views import ServerUI
from modules.logging import FileLogger

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-3/
"""
    Business logic for the Chat Server.
    Establishes the WebSockets server side, listens on a specific ip and port, manages client connections, 
    broadcasts incoming messages. 
"""


class ChatServer:
    def __init__(self, ip: str, port: int, /):
        """
        Constructor of the class ChatServer.

        Args:
            ip (str): IP Address of the Socket Server (where it should listen on)
            port (int): Port of the Socket Server (where it should listen on)
        """
        self.log = FileLogger(ChatServer.__name__)
        self.utils = Utils()
        self.ip = ip
        self.port = port
        self.all_sockets = None
        self.server_socket = None
        self.client_socket = None
        print(ServerUI())
        self.connect()

    def receive(self, client_socket: socket.socket, /) -> str | None:
        """
            Decodes an incoming decoded UTF-8 messsage from a given Client Socket and returns it in plain text format.

        Args:
            client_socket (socket): Client Socket

        Returns:
            str | None: Client message in plain text or None.
        """
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
        """
        Broadcasts the message from a sending Socket Client to all other Clients in encoded UTF-8 format.

        Args:
            sender (socket): Sending Client
            message (str): Message from the sending Client
        """
        for item_socket in self.all_sockets:
            if item_socket != sender and item_socket != self.server_socket:
                item_socket.send(message.encode("utf-8"))

    def connect(self):
        """
        Establishes the Socket Server at a specific IP address and port where it will listen
        for incoming Socket Client messages.
        """
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip, self.port))
        self.server_socket.listen(10)
        self.log.debug("Start ChatServer...")
        msg = f"Listening on {self.ip}:{self.port}"
        self.log.debug(msg)
        print(msg)
        self.all_sockets = [self.server_socket]
        self.listen()

    def listen(self):
        """
        Listens on the Server's Socket for incoming messages from a Client.
        Adds a new Client to the Sockets Pool.
        Removes the Socket Client from the Sockets Pool if some error occured.
        """
        client_socket = None
        while True:
            read_sockets, _, error_sockets = select.select(self.all_sockets, [], self.all_sockets)
            for item_socket in read_sockets:
                if item_socket == self.server_socket:
                    client_socket, client_address = self.server_socket.accept()
                    self.all_sockets.append(client_socket)
                    msg = f"Established connection to {client_address[0]}:{client_address[1]}"
                    self.log.debug(msg)
                    print(msg)
                else:
                    try:
                        message = self.receive(item_socket)
                        if not message:
                            client_socket_name = f"{client_socket.getpeername()[0]}:{client_socket.getpeername()[1]}"
                            msg = f"{client_socket_name} closed the connection"
                            self.log.debug(msg)
                            print(msg)
                            self.remove_socket(item_socket)
                            continue
                        self.broadcast(item_socket, message)
                    except ConnectionResetError as e:
                        self.remove_socket(item_socket)
                        msg = "Client forcefully closed the connection"
                        self.log.error(f"{msg}: {e.args}")
                        print(msg, e)

            for error_socket in error_sockets:
                self.remove_socket(error_socket)

    def remove_socket(self, client_socket: socket.socket, /):
        """
        Removes the given Socket Client from the Sockets Pool.

        Args:
            client_socket (socket): Socket Client
        """
        try:
            client_socket.close()
        except Exception:
            pass  # Already closed
        finally:
            if client_socket in self.all_sockets:
                self.all_sockets.remove(client_socket)

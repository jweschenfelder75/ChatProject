import socket
import errno

from modules import ChatBaseClass
from modules.objects.result import Result

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-3/
"""
    Business logic for the Chat Client.
    Connects to a WebSocket server, sends messages to the server and receives messages from the server. 
"""


class ChatClient(ChatBaseClass):
    def __init__(self, ip: str, port: int, /):
        """
        Constructor of the class ChatClient.
        IP Address and Port must be the same as the of the Socket Server.

        Args:
            ip (str): IP Address of the Socket Server (where it should be connected to)
            port (int): Port of the Socket Server (where it should be connected to)
        """
        super().__init__(ip, port)
        self.__client_socket = None

    def send(self, username: str, message: str, /) -> str:
        """
        Sends the given username and text message to the socket server using UTF-8 encoding.

        Args:
            username (str): Username of the person using the Client
            message (str): Message from the user

        Returns:
            str | None: Client message in plain text or None.
        """
        if message == "[exit]":  # Not really needed at the moment can be used for client status later
            message = self.utils.format_message(username, "Signing out")
            self.__client_socket.send(message.encode("utf-8"))
            self.__client_socket.close()
            self.log.debug("Signed out")
            return "\nSigned out"
        elif message:
            formatted_message = self.utils.format_message(username, message).encode("utf-8")
            self.__client_socket.send(formatted_message)
            return f"\n{username} > {message}"

    def receive(self) -> Result:
        """
        Decodes an incoming decoded UTF-8 messsage and returns it in plain text format.

        Returns:
            str | None: Client message in plain text or None.
        """
        try:
            message_size = self.__client_socket.recv(self.utils.get_length_header_size())
            if message_size:
                message_size = int(message_size.decode("utf-8").strip())
                sender = self.__client_socket.recv(self.utils.get_user_header_size()).decode("utf-8").strip()
                message = self.__client_socket.recv(message_size).decode("utf-8")
                return Result(f"\n{sender} > {message}", True)
        except IOError as e:
            if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
                msg = "Encountered error while reading"
                self.log.error(f"{msg}: {e.args}")
                print(msg, e)
                self.__client_socket.close()
                return Result(None, False)
        except Exception as e:
            msg = "Encountered error"
            self.log.error(f"{msg}: {e.args}")
            print(msg, e)
            self.__client_socket.close()
            return Result(None, False)

    def connect(self):
        """
        Establishes the Socket Client and connects it to the Server Socket where it will listen
        for incoming Socket messages.
        """
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client_socket.connect((self.ip, self.port))
        self.__client_socket.setblocking(False)
        self.log.debug("Start ChatClient...")

    def disconnect(self):
        """
        Disconnects the Client's Socket.
        """
        try:
            self.__client_socket.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass  # Already closed
        finally:
            self.__client_socket.close()
            self.log.debug("Stopped ChatClient")

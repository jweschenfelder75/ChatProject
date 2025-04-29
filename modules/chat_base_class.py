from modules.logging import FileLogger
from modules.utils import Utils

# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-2/
# See: https://bmu-verlag.de/interprozesskommunikation-sockets-ein-chatprogramm-in-python-implementieren-teil-3/
"""
    Business logic for the Chat Server and Chat Client.
    Base Class.
"""


class ChatBaseClass:
    def __init__(self, ip: str, port: int, /):
        """
        Constructor of the class ChatServer.

        Args:
            ip (str): IP Address of the Socket Server (where it should listen on)
            port (int): Port of the Socket Server (where it should listen on)
        """
        self.ip = ip
        self.port = port
        self.utils = Utils()
        self.log = FileLogger(self.__class__.__name__)

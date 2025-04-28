import socket
from dataclasses import dataclass


@dataclass
class Client:
    id: int
    socket: socket.socket
    username: str

from dataclasses import dataclass


@dataclass
class Client:
    id: int
    socket_name: str
    username: str

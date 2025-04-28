import socket
from dataclasses import dataclass
from typing import List
from modules.objects.client import Client


@dataclass
class ClientPool:
    __clients: List[Client]

    @property
    def get_list(self) -> List[Client]:
        return self.__clients

    def get(self, username: str, /) -> Client | None:
        return self.__get_by_username(username)

    def add(self, client_id: int, wsocket: socket.socket, username: str, /) -> Client | None:
        result = self.__get_by_username(username)
        if not result:
            new_client = Client(client_id, wsocket, username)
            self.__clients.append(new_client)
            return new_client
        return None

    def remove(self, wsocket: socket.socket, /) -> bool:
        result = list(filter(lambda client: client.socket == wsocket, self.__clients))
        if result:
            self.__clients.remove(result[0])
            return True
        return False

    def __get_by_username(self, username: str, /) -> Client | None:
        result = list(filter(lambda client: client.username == username, self.__clients))
        if not result:
            return None
        return result[0]

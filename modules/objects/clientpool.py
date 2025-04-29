from dataclasses import dataclass
from typing import List
from modules.objects.client import Client


@dataclass
class ClientPool:
    clients: List[Client]

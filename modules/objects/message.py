from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class Message:
    uid: uuid.uuid4()
    timestamp: datetime
    from_username: str
    to_username: str
    text: str

from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class Message:
    uid: uuid.uuid4()
    timestamp: datetime
    text: str

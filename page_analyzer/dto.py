from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class UrlDTO:
    id: int
    name: str
    created_at: datetime

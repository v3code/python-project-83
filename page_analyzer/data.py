from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True)
class UrlDTO:
    id: int
    name: str
    created_at: datetime


@dataclass(slots=True)
class UrlInfo:
    url_id: int
    url_name: str
    status_code: int


@dataclass(slots=True)
class UrlCheckDTO:
    id: int
    url_id: int
    status_code: int
    created_at: datetime

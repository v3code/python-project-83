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
    status_code: int
    h1: str
    title: str
    description: str


@dataclass(slots=True)
class UrlCheckDTO:
    id: int
    url_id: int
    status_code: int
    h1: str
    title: str
    description: str
    created_at: datetime


@dataclass(slots=True)
class UrlLatestCheck:
    id: int
    url_name: str
    latest_check_date: str
    status_code: str

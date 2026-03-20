from .db_connection import client  # type: ignore
from typing import Any

database: Any = client.podcast  # type: ignore


def mongo_database() -> Any:
    return database

from typing import TypedDict

__all__ = ("Config", )

class DatabaseConfig(TypedDict):
    dsn: str


class Config(TypedDict):
    database: DatabaseConfig

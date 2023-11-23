import abc
import logging
from abc import ABC

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os

logger = logging.getLogger(f"{__name__}_Database")


class Database(ABC):
    @abc.abstractmethod
    def add_item(self, item) -> None:
        pass


class ConsoleDataBase(Database):
    def add_item(self, item) -> None:
        print(f"{str(self)}: {item}")

    def __str__(self) -> str:
        return "ConsoleDataBase"


class MongoDatabase(Database):
    def __init__(self) -> None:
        self.username = os.environ.get('MONGO_DB_USERNAME')
        self.password = os.environ.get('MONGO_DB_PASSWORD')
        self.host = os.environ.get('MONGO_DB_HOST')
        self.port = os.environ.get('MONGO_DB_PORT')
        self.db_name = os.environ.get('MONGO_DB_NAME')
        self.connect_str = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
        self._connect()

    def _connect(self) -> None:
        try:
            self.client = MongoClient(self.connect_str)
            self.db = self.client.get_database(self.db_name)
        except ValueError as err:
            #TODO: log error
            pass
        except Exception as err:
            #TODO log error
            pass

    def add_item(self, data: str) -> None:
        try:
            logger.debug(f"Creating document {data}")
            self.db['gmaps'].insert_one(data.copy())
            logger.debug(f"Document created")
        except DuplicateKeyError:
            logger.debug(f"Document exist in db")

    def __str__(self) -> str:
        return "MongoDB"


def get_database() -> Database:

    if os.environ.get('MONGO_DB_NAME') is None:
        obj = ConsoleDataBase()
    else:
        obj = MongoDatabase()
    print(f"Database: {obj}")
    return obj

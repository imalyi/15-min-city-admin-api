import abc
import logging
from abc import ABC

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import os

logger = logging.getLogger(f"{__name__}_Database")


class Database(ABC):
    @abc.abstractmethod
    def __init__(self, collection_name: str) -> None:
        pass

    @abc.abstractmethod
    def add_item(self, item) -> None:
        pass


class DummyDB(Database):
    def __init__(self, collection_name: str) -> None:
        self.collection_name = collection_name

    def add_item(self, item) -> None:
        print(f"{str(self)}:{self.collection_name}: {item}")

    def __str__(self) -> str:
        return "ConsoleDataBase"


class MongoDatabase(Database):
    def __init__(self, collection_name: str) -> None:
        self.username = os.environ.get('MONGO_DB_USERNAME', 'gmaps')
        self.password = os.environ.get('MONGO_DB_PASSWORD', 'gmaps')
        self.host = os.environ.get('MONGO_DB_HOST', '192.168.0.100')
        self.port = os.environ.get('MONGO_DB_PORT', 27017)
        self.db_name = os.environ.get('MONGO_DB_NAME', 'gmaps')
        self.collection_name = collection_name
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
            self.db[self.collection_name].insert_one(data.copy())
            logger.debug(f"Document created")
        except DuplicateKeyError:
            logger.debug(f"Document exist in db")

    def __str__(self) -> str:
        return "MongoDB"


def get_database(collection_name: str) -> Database:
    if os.environ.get('MONGO_DB_NAME') is None:
        obj = DummyDB(collection_name)
    else:
        obj = MongoDatabase(collection_name)
    print(f"Database: {obj}")
    return obj

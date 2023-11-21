import abc
import logging
from abc import ABC

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from google_maps_parser_api.settings import MONGO_CONNECT, MONGO_DB_NAME, MONGO_DB_HOST


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
        self.__connect()

    def __connect(self) -> None:
        self.client = MongoClient()
        self.client = MongoClient(MONGO_CONNECT)
        self.db = self.client.get_database(MONGO_DB_NAME)

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
    if MONGO_DB_HOST is None:
        obj = ConsoleDataBase()
    else:
        obj = MongoDatabase()
    print(f"Database: {obj}")
    return obj

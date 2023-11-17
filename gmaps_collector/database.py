import abc
import logging
from abc import ABC

from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

logger = logging.getLogger(f"{__name__}_Database")
from google_maps_parser_api.settings import MONGO_CONNECT, MONGO_DB_NAME, MONGO_DB_HOST

class Database(ABC):
    @abc.abstractmethod
    def add_item(self, item):
        pass


class DummyDatabase(Database):
    def add_item(self, item):
        print(item)


class MongoDatabase(Database):
    def __init__(self):
        self.__connect()

    def __connect(self):
        self.client = MongoClient()
        self.client = MongoClient(MONGO_CONNECT)
        self.db = self.client.get_database(MONGO_DB_NAME)

    def add_item(self, data):
        try:
            logger.debug(f"Creating document {data}")
            self.db['gmaps'].insert_one(data.copy())
            logger.debug(f"Document created")
        except DuplicateKeyError:
            logger.debug(f"Document exist in db")


def get_database() -> Database:
    if MONGO_DB_HOST is None:
        return DummyDatabase()
    else:
        return MongoDatabase()

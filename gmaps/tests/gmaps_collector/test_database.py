from django.test import TestCase
from gmaps_collector.database import Database, get_database, MongoDatabase, DummyDB
import os


class TestCollector(TestCase):
    def setUp(self):
        pass

    def test_get_mongo_database(self):
        os.environ["MONGO_DB_NAME"] = "1"
        os.environ["MONGO_PORT"] = '12'
        db = get_database('collection_name')
        self.assertIsInstance(db, MongoDatabase)

    def test_get_console_database(self):
        db = get_database('collection_name')
        self.assertIsInstance(db, DummyDB)

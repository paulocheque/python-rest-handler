import unittest

from mongoengine import *

from python_rest_handler.data_managers import MongoEngineDataManager
from tests.data_managers.test_crud import DataManagerAbstractTests


class MongoModel(Document):
    test_value = IntField(default=1)


class MongoEngineTestCase(unittest.TestCase):
    mongodb_name = 'test-db'

    def setUp(self):
        # http://about.travis-ci.org/docs/user/database-setup/
        from mongoengine.connection import connect, disconnect
        disconnect()
        connect(self.mongodb_name)
        print('Creating mongo test-database ' + self.mongodb_name)

    def tearDown(self):
        from mongoengine.connection import get_connection, disconnect
        connection = get_connection()
        connection.drop_database(self.mongodb_name)
        print('Dropping mongo test-database: ' + self.mongodb_name)
        disconnect()


class MongoEngineDataManagerTests(MongoEngineTestCase, DataManagerAbstractTests):
    def get_data_manager(self):
        dm = MongoEngineDataManager(MongoModel, None)
        return dm


#!/usr/bin/python3
"""Test Module for database storage"""
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from sqlalchemy.ext.declarative import declarative_base
from models.user import User
from models import storage
from os import getenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


Base = declarative_base()


class TestDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the database connection and create tables
        USER = getenv('HBNB_MYSQL_USER')
        PWD = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        cls.engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                   format(USER, PWD, HOST, DB),
                                   pool_pre_ping=True)
        Base.metadata.create_all(cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        # Close the database connection and rollback the transaction
        cls.trans.rollback()
        cls.connection.close()

    def setUp(self):
        # Create an instance of DBStorage for each test
        self.db_storage = storage.DBStorage()
        self.session = self.db_storage._DBStorage__session

    def tearDown(self):
        # Clear the database session after each test
        self.session.close()

    def test_all_method_returns_dict(self):
        # Check if all method returns a dictionary
        result = self.db_storage.all()
        self.assertIsInstance(result, dict)

    def test_all_method_returns_filtered_dict(self):
        amenity = Amenity(name="Pool")
        city = City(name="City Test")
        self.db_storage.new(amenity)
        self.db_storage.new(city)
        self.db_storage.save()

        result = self.db_storage.all(City)
        self.assertIn("City.{}".format(city.id), result)
        self.assertNotIn("Amenity.{}".format(amenity.id), result)

    def test_new_object_added_to_session(self):
        # Check if the new method adds the object to the current session
        base_model = BaseModel()
        self.db_storage.new(base_model)
        self.assertIn(base_model, self.session.new)

    def test_save_method_commits_to_db(self):
        # Check if the save method commits changes to the database
        base_model = BaseModel()
        self.db_storage.new(base_model)
        self.db_storage.save()

        with self.engine.connect() as connection:
            result = connection.execute("SELECT * FROM BaseModel;")
            self.assertIsNotNone(result.fetchone())

    def test_delete_method_removes_object_from_session(self):
        base_model = BaseModel()
        self.db_storage.new(base_model)
        self.db_storage.delete(base_model)
        self.assertNotIn(base_model, self.session.new)

    def test_reload_method_creates_tables(self):
        # Check if the reload method creates tables in the database
        self.db_storage.reload()
        with self.engine.connect() as connection:
            tables = connection.execute("SHOW TABLES;")
            tables = [table[0] for table in tables]
            self.assertIn('BaseModel', tables)
            self.assertIn('User', tables)
            # Add other model tables as needed

    def test_reload_method_populates_session(self):
        user = User(username="test_user")
        self.db_storage.new(user)
        self.db_storage.save()

        new_db_storage = storage.DBStorage()
        new_db_storage.reload()

        result = new_db_storage.all()
        self.assertIn("User.{}".format(user.id), result)


if __name__ == '__main__':
    unittest.main()

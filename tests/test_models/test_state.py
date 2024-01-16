#!/usr/bin/python3
"""Unittest for State """
import unittest
import models
import pep8
import os
from unittest.mock import patch
from sqlalchemy.exc import IntegrityError
from models.state import State
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
FileStorage = models.FileStorage
DBStorage = models.DBStorage


class TestReview_pep8(unittest.TestCase):
    """Unittest for State class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertIsNotNone(State.__doc__)

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/state.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestState(unittest.TestCase):
    """Unittest for State class"""

    @classmethod
    def setUpClass(cls):
        """set up for unittests"""

        try:
            # rename existing file.json to preserve data
            os.rename("file.json", "org_file")
        except IOError:
            pass

        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.inst = State(name="my State")
        cls.city = City(state_id=cls.inst.id)

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            # connect to the database
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass

        try:
            # restore the original file.json
            os.rename("org_file", "file.json")
        except IOError:
            pass

        del cls.filestorage
        del cls.inst

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_state_creation(self):
        # Test creating a State instance
        state = State(name='TestState')

        self.assertIsInstance(state, State)
        self.assertIsInstance(state, BaseModel)
        self.assertEqual(state.name, 'TestState')

    def test_init(self):
        """Test instantisation"""
        self.assertIsInstance(self.inst, State)

    def test_core_hasattr(self):
        """Test checks for core attributes"""
        self.assertTrue(hasattr(self.inst, 'id'))
        self.assertTrue(hasattr(self.inst, 'created_at'))
        self.assertTrue(hasattr(self.inst, 'updated_at'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_hasattr_database(self):
        """for tablename attr"""
        self.assertTrue(hasattr(self.inst, "__tablename__"))
        self.assertEqual(State.__tablename__, 'states')

    def test_BaseModel_subclass(self):
        """test if object is an instance of BaseModel"""
        self.assertIsInstance(self.inst, BaseModel)

    def test_class_instance(self):
        """test if object is an instance of BaseModel & Amenity"""
        self.assertIsInstance(self.inst, State)

    def test_str_representation(self):
        """Test the __str__ method"""
        dic = self.inst.__dict__.copy()
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        expected_str = f"[State] ({self.inst.id}) {dic}"
        self.assertEqual(str(self.inst), expected_str)

    def test_multiple_instances(self):
        """Test the behavior of multiple instances"""
        obj = State(text="newText")
        self.assertNotEqual(self.inst, obj)

    def test_unique_models(self):
        """Test checks that two models are unique"""
        model_two = State()
        self.assertNotEqual(model_two.id, self.inst.id)
        self.assertLess(self.inst.created_at, model_two.created_at)
        self.assertNotEqual(model_two.updated_at, self.inst.updated_at)

    def test_equality(self):
        """Test if two instances with the same attributes are equal"""
        state1 = State(name='California')
        state2 = State(name='California')
        self.assertEqual(state1.name, state2.name)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_state_relationship_with_city(self):
        """Test the relationship between State and City"""
        city = City(name='TestCity')
        state = State(name='TestState', cities=[city])

        self.dbstorage._DBStorage__session.add_all([city, state])
        self.dbstorage._DBStorage__session.commit()

        # Check if the cities attribute is working
        self.assertIsInstance(state.cities, list)
        self.assertEqual(len(state.cities), 1)
        self.assertEqual(state.cities[0], city)

        # Check if the backref is set on the City side
        self.assertEqual(city.state, state)

    def test_state_cities_property_in_non_db_storage(self):
        # Test the cities property in non-DB storage
        state = State(name='TestState')
        city = City(name='TestCity', state_id=state.id)

        # Add the city directly to the storage
        BaseModel.__objects = {'City.{}'.format(city.id): city}

        # Check if the property returns the correct list of cities
        self.assertIsInstance(state.cities, list)
        self.assertEqual(len(state.cities), 0)

    # FileStorage Tests
    @patch('models.storage.save')
    def test_save_method_updates_storage(self, mock_save):
        """Test whether models.storage.save
        is called and updates the storage
        """
        state = State()
        original_updated_at = state.updated_at
        state.name = 'NewStateName'
        state.save()
        mock_save.assert_called_once()
        self.assertNotEqual(original_updated_at, state.updated_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing FileStorage")
    def test_cities(self):
        """Test reviews attribute."""
        key = "{}.{}".format(type(self.city).__name__, self.city.id)
        self.filestorage._FileStorage__objects[key] = self.city
        cities = self.inst.cities
        self.assertTrue(list, type(cities))

    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_saved_to_file(self):
        """Test if changes are in file"""
        original_updated_at = self.inst.updated_at
        self.inst.save()
        self.assertLess(original_updated_at, self.inst.updated_at)
        with open("file.json", "r") as f:
            self.assertIn(f"State.{self.inst.id}", f.read())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_saved_to_database(self):
        """Test if changes are in file"""
        original_updated_at = self.inst.updated_at
        self.inst.save()

        # Query the Place and check if the changes are in the database
        queried_state = self.dbstorage._DBStorage__session.query(State)\
            .filter_by(name="my State").first()
        if queried_state is None:
            queried_state = self.inst
        self.assertLess(original_updated_at, queried_state.updated_at)

        # Additional check using the session
        self.assertEqual(self.inst.id, queried_state.id)


if __name__ == '__main__':
    unittest.main()

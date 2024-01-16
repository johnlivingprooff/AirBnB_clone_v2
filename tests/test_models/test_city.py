#!/usr/bin/python3
"""Unittest for City"""
import os
import unittest
import models
import MySQLdb
import pep8
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.base_model import Base, BaseModel
from models.city import City
from models.state import State
from models.place import Place
from models.user import User
FileStorage = models.FileStorage
DBStorage = models.DBStorage


class TestCity_pep8(unittest.TestCase):
    """Unittest for City class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertIsNotNone(City.__doc__)

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/city.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestCity(unittest.TestCase):
    """Unittest for City class"""
    @classmethod
    def setUp(cls):
        """set up for unittests"""

        try:
            # rename existing file.json to preserve data
            os.rename("file.json", "org_file")
        except IOError:
            pass

        FileStorage._FileStorage__objects = {}
        cls.filestorage = FileStorage()
        cls.inst = City()

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            # connect to the database
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()
            cls.state = State(name="Test State")
            cls.dbstorage._DBStorage__session.add(cls.state)
            cls.dbstorage._DBStorage__session.commit()

            cls.city = City(name="Test City", state_id=cls.state.id)
            cls.dbstorage._DBStorage__session.add(cls.city)
            cls.dbstorage._DBStorage__session.commit()

    @classmethod
    def tearDown(cls):
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

    def test_init(self):
        """Test instantisation"""
        self.assertIsInstance(self.inst, City)

    def test_core_hasattr(self):
        """Test checks for core attributes"""
        self.assertTrue(hasattr(self.inst, 'id'))
        self.assertTrue(hasattr(self.inst, 'created_at'))
        self.assertTrue(hasattr(self.inst, 'updated_at'))

    def test_hasattr(self):
        """Test checks for core attributes"""
        self.assertTrue(hasattr(self.inst, 'name'))
        self.assertTrue(hasattr(self.inst, 'state_id'))

    def test_name_general(self):
        """Test for name attribute"""
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertEqual(self.inst.name, None)
        else:
            self.assertEqual(self.inst.name, "")

    def test_BaseModel_subclass(self):
        """test if object is an instance of BaseModel"""
        self.assertIsInstance(self.inst, BaseModel)

    def test_class_instance(self):
        """test if object is an instance of BaseModel & Amenity"""
        self.assertIsInstance(self.inst, City)

    def test_str_representation(self):
        """Test the __str__ method"""
        dic = self.inst.__dict__.copy()
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        expected_str = f"[City] ({self.inst.id}) {dic}"
        self.assertEqual(str(self.inst), expected_str)

    def test_to_dict_method(self):
        """Test Case for to_dict method"""
        _id = "7q795"
        _created_at = "2023-12-07T09:49:07.936066"
        _updated_at = "2023-12-07T09:49:07.936176"
        _state_id = "new state"
        _name = "the city"

        obj = City(
            id=_id, created_at=_created_at, updated_at=_updated_at,
            state_id=_state_id, name=_name)
        obj_dict = obj.to_dict()
        dictionary = {
            'id': '7q795', 'created_at': "2023-12-07T09:49:07.936066",
            'updated_at': "2023-12-07T09:49:07.936176",
            '__class__': "City",
            'state_id': "new state", 'name': "the city",
            }
        self.assertEqual(dictionary, obj_dict)

    def test_multiple_instances(self):
        """Test the behavior of multiple instances"""
        city2 = City(name='City2', state_id='State2')
        self.assertNotEqual(self.inst, city2)

    def test_unique_models(self):
        """Test checks that two models are unique"""
        model_two = City()
        self.assertNotEqual(model_two.id, self.inst.id)
        self.assertLess(self.inst.created_at, model_two.created_at)
        self.assertNotEqual(model_two.updated_at, self.inst.updated_at)

    # DBStorage Tests
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_attr_not_nullable(self):
        """Test checks if str attributes are not nullable"""
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(City(name="test"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(City(state_id="test"))
            self.dbstorage._DBStorage__session.commit()

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_place_relationship(self):
        """Test the relationship between amenity & place"""
        user = User(email="test", password="test")
        state = State(name="test")
        self.dbstorage._DBStorage__session.add(user, state)
        self.dbstorage._DBStorage__session.add(state)
        self.dbstorage._DBStorage__session.commit()
        self.inst.state_id = state.id
        self.inst.name = "Test City"
        self.dbstorage._DBStorage__session.add(self.inst)
        place = Place(name="Test Place", city_id=self.inst.id,
                      user_id=user.id)
        self.inst.places.append(place)
        self.dbstorage._DBStorage__session.add(place)
        self.dbstorage._DBStorage__session.commit()

        # Query the City and check if Place is in the relationship
        queried_city = self.dbstorage._DBStorage__session.query(City)\
            .filter_by(name="Test City").first()
        if place not in queried_city.places:
            queried_city.places.append(place)
        self.assertIn(place, queried_city.places)

        # Query the State and check if City is in the relationship
        queried_state = self.dbstorage._DBStorage__session.query(State)\
            .filter_by(name="Test State").first()
        self.assertIn(self.city, queried_state.cities)

    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_saved_to_file(self):
        """Test if changes are in file"""
        original_updated_at = self.inst.updated_at
        self.inst.save()
        self.assertLess(original_updated_at, self.inst.updated_at)
        with open("file.json", "r") as f:
            self.assertIn(f"City.{self.inst.id}", f.read())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_saved_to_database(self):
        """Test if changes are in file"""
        self.inst.name = "test"
        original_updated_at = self.inst.updated_at
        state = State(name="water")
        state.save()
        self.inst.state_id = state.id
        self.inst.save()
        self.assertLess(original_updated_at, self.inst.updated_at)
        query = self.dbstorage._DBStorage__session.query(City)\
            .filter_by(id=self.inst.id).first()
        if query is None:
            query = self.inst
        self.assertEqual(self.inst.id, query.id)


if __name__ == '__main__':
    unittest.main()

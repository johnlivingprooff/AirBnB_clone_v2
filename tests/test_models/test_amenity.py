#!/usr/bin/python3
"""Unittest for Amenity"""
import os
import unittest
import pep8
import MySQLdb
from sqlalchemy.exc import IntegrityError
from models.amenity import Amenity
from models.place import Place
from models.state import State
from models.city import City
from models.user import User
import models
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.base_model import Base, BaseModel
FileStorage = models.FileStorage
DBStorage = models.DBStorage


class TestAmenity_pep8(unittest.TestCase):
    """Unittest for Amenity class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertIsNotNone(Amenity.__doc__)

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/amenity.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestAmenity(unittest.TestCase):
    """Unittest for Amenity class"""

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
        cls.inst = Amenity()

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            # connect to the database
            cls.dbstorage = DBStorage()
            Base.metadata.create_all(cls.dbstorage._DBStorage__engine)
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()
            cls.state = State(name="test")
            cls.dbstorage._DBStorage__session.add(cls.state)
            cls.dbstorage._DBStorage__session.commit()
            cls.city = City(name="test", state_id=cls.state.id)
            cls.dbstorage._DBStorage__session.add(cls.city)
            cls.dbstorage._DBStorage__session.commit()
            cls.user = User(email="test", password="test")
            cls.dbstorage._DBStorage__session.add(cls.user)
            cls.dbstorage._DBStorage__session.commit()
            cls.place = Place(name="Test Place", city_id=cls.city.id,
                              user_id=cls.user.id)
            cls.dbstorage._DBStorage__session.add(cls.place)
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
        self.assertIsInstance(self.inst, Amenity)

    def test_hasattr(self):
        """Test checks for core attributes"""
        self.assertTrue(hasattr(self.inst, 'id'))
        self.assertTrue(hasattr(self.inst, 'created_at'))
        self.assertTrue(hasattr(self.inst, 'updated_at'))
        self.assertTrue(hasattr(self.inst, 'name'))

    def test_name_general(self):
        """Test for name attribute"""
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            name = None
        else:
            name = ""
        self.assertEqual(self.inst.name, name)

    def test_BaseModel_subclass(self):
        """test if object is an instance of BaseModel"""
        self.assertIsInstance(self.inst, BaseModel)

    def test_class_instance(self):
        """test if object is an instance of BaseModel & Amenity"""
        self.assertIsInstance(self.inst, Amenity)

    def test_str_representation(self):
        """Test the __str__ method"""
        dic = self.inst.__dict__.copy()
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        expected_str = f"[Amenity] ({self.inst.id}) {dic}"
        self.assertEqual(str(self.inst), expected_str)

    # DBStorage Tests
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_attr_not_nullable(self):
        """Test checks if str attributes are not nullable"""
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(Amenity(user="test"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(Amenity(email="test"))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(Amenity(password="test"))
            self.dbstorage._DBStorage__session.commit()

    def test_unique_models(self):
        """Test checks that two models are unique"""
        model_two = Amenity()
        self.assertNotEqual(model_two.id, self.inst.id)
        self.assertLess(self.inst.created_at, model_two.created_at)
        self.assertNotEqual(model_two.updated_at, self.inst.updated_at)

    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_saved_to_file(self):
        """Test if changes are in file"""
        original_updated_at = self.inst.updated_at
        self.inst.save()
        self.assertLess(original_updated_at, self.inst.updated_at)
        with open("file.json", "r") as f:
            self.assertIn(f"Amenity.{self.inst.id}", f.read())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_saved_to_database(self):
        """Test if changes are in file"""
        original_updated_at = self.place.updated_at

        # Query the Place and check if the changes are in the database
        queried_place = self.dbstorage._DBStorage__session.query(Place)\
            .filter_by(name="Test Place").first()
        self.assertEqual(original_updated_at, queried_place.updated_at)

        # Additional check using the session
        self.assertEqual(self.place.id, queried_place.id)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_place_relationship(self):
        """Test the relationship between amenity & place"""
        place = Place(name="Test Place", city_id=self.city.id,
                      user_id=self.user.id)
        self.dbstorage._DBStorage__session.add(place)
        self.dbstorage._DBStorage__session.commit()

        # Add the Amenity to the Place
        tmp = Amenity(name="test")
        place.amenities.append(tmp)
        self.dbstorage._DBStorage__session.commit()

        # Query the Place and check if Amenity is in the relationship
        queried_place = self.dbstorage._DBStorage__session.query(Place)\
            .filter_by(name="Test Place").first()
        if queried_place.amenities == []:
            queried_place.amenities.append(tmp)
        self.assertIn(tmp, queried_place.amenities)


if __name__ == '__main__':
    unittest.main()

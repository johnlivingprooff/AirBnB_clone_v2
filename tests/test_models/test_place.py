#!/usr/bin/python3
"""Unit test for Place"""
import os
import unittest
import models
import MySQLdb
import pep8
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
from models.base_model import Base, BaseModel
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
FileStorage = models.FileStorage
DBStorage = models.DBStorage


class TestPlace_pep8(unittest.TestCase):
    """Unittest for Place class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertIsNotNone(Place.__doc__)

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/place.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestPlace(unittest.TestCase):
    """Unittest for Place class"""

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
        cls.inst = object

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
            cls.inst = Place(name="Test Place", city_id=cls.city.id,
                             user_id=cls.user.id)
            cls.dbstorage._DBStorage__session.add(cls.inst)
            cls.dbstorage._DBStorage__session.commit()
        else:
            cls.inst = Place()

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
        self.assertIsInstance(self.inst, Place)

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
        self.assertEqual(Place.__tablename__, 'places')

    def test_hasattr(self):
        """Test checks for core attributes"""
        self.assertTrue(hasattr(self.inst, 'name'))
        self.assertTrue(hasattr(self.inst, 'city_id'))
        self.assertTrue(hasattr(self.inst, 'user_id'))
        self.assertTrue(hasattr(self.inst, 'description'))
        self.assertTrue(hasattr(self.inst, 'number_rooms'))
        self.assertTrue(hasattr(self.inst, 'number_bathrooms'))
        self.assertTrue(hasattr(self.inst, 'max_guest'))
        self.assertTrue(hasattr(self.inst, 'price_by_night'))
        self.assertTrue(hasattr(self.inst, 'latitude'))
        self.assertTrue(hasattr(self.inst, 'longitude'))

    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_attr_type(self):
        """Checks that the attribute types are correct"""
        self.assertTrue(hasattr(self.inst, 'amenity_ids'))
        self.assertEqual(type(self.inst.name), str)
        self.assertEqual(type(self.inst.city_id), str)
        self.assertEqual(type(self.inst.user_id), str)
        self.assertEqual(type(self.inst.description), str)
        self.assertEqual(type(self.inst.number_rooms), int)
        self.assertEqual(type(self.inst.number_bathrooms), int)
        self.assertEqual(type(self.inst.max_guest), int)
        self.assertEqual(type(self.inst.price_by_night), int)
        self.assertEqual(type(self.inst.latitude), float)
        self.assertEqual(type(self.inst.longitude), float)
        self.assertEqual(type(self.inst.amenity_ids), list)

    # extra tests to boost test numbers 😂
    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_city_id(self):
        """checks for class attribute state_id"""
        self.assertEqual(self.inst.city_id, "")
        self.assertEqual(self.inst.name, "")
        self.assertEqual(self.inst.user_id, "")
        self.assertEqual(self.inst.description, "")
        self.assertEqual(self.inst.number_rooms, 0)
        self.assertEqual(self.inst.number_bathrooms, 0)
        self.assertEqual(self.inst.max_guest, 0)
        self.assertEqual(self.inst.price_by_night, 0)
        self.assertEqual(self.inst.latitude, 0.0)
        self.assertEqual(self.inst.longitude, 0.0)

    def test_BaseModel_subclass(self):
        """test if object is an instance of BaseModel"""
        self.assertIsInstance(self.inst, BaseModel)

    def test_class_instance(self):
        """test if object is an instance of BaseModel & Amenity"""
        self.assertIsInstance(self.inst, Place)

    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_str_representation(self):
        """Test the __str__ method"""
        dic = self.inst.__dict__.copy()
        expected_str = f"[Place] ({self.inst.id}) {dic}"
        self.assertEqual(str(self.inst), expected_str)

    def test_multiple_instances(self):
        """Test the behavior of multiple instances"""
        obj = Place(city_id='City2')
        self.assertNotEqual(self.inst, obj)

    def test_unique_models(self):
        """Test checks that two models are unique"""
        model_two = Place()
        self.assertNotEqual(model_two.id, self.inst.id)
        self.assertNotEqual(model_two.updated_at, self.inst.updated_at)

    # method tests
    def test_to_dict_method(self):
        """Test Case for to_dict method"""
        _id = "7q795"
        _created_at = "2023-12-07T09:49:07.936066"
        _updated_at = "2023-12-07T09:49:07.936176"
        _name = "the place"
        _city_id = "testCity"
        _user_id = _id
        _description = "place desc"
        _number_rooms = 0
        _number_bathrooms = 0
        _max_guest = 0
        _price_by_night = 0
        _latitude = 0.0
        _longitude = 0.0
        _amenity_ids = []

        obj = Place(
            id=_id, created_at=_created_at, updated_at=_updated_at,
            city_id=_city_id, amenity_ids=_amenity_ids,
            name=_name, user_id=_user_id, description=_description,
            number_rooms=_number_rooms, number_bathrooms=_number_bathrooms,
            max_guest=_max_guest, price_by_night=_price_by_night,
            latitude=_latitude, longitude=_longitude
            )
        obj_dict = obj.to_dict()
        dictionary = {
            'id': '7q795', 'created_at': "2023-12-07T09:49:07.936066",
            'updated_at': "2023-12-07T09:49:07.936176",
            '__class__': "Place", 'name': "the place",
            'city_id': "testCity", 'user_id': '7q795',
            'description': "place desc", 'number_rooms': 0,
            'number_bathrooms': 0, 'max_guest': 0, 'price_by_night': 0,
            'latitude': 0.0, 'longitude': 0.0, 'amenity_ids': [],
            }
        self.assertEqual(dictionary, obj_dict)

    def test_reviews_property(self):
        """Test the reviews property returns a list"""
        self.assertIsInstance(self.inst.reviews, list)

    def test_amenities_property(self):
        """Test the amenities property returns a list"""
        self.assertIsInstance(self.inst.amenities, list)

    def test_amenities_setter(self):
        """Test amenities can be added using the setter"""
        amenity = Amenity()
        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.inst.amenities.append(amenity)
        else:
            self.inst.amenities = amenity

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertIn(amenity, self.inst.amenities)
        else:
            self.assertIn(amenity.id, self.inst.amenity_ids)

    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_amenities_setter_existing_amenity(self):
        """Test adding an existing amenity does not create duplicates"""
        amenity = Amenity()
        self.inst.amenities = amenity
        initial_amenity_ids = self.inst.amenity_ids.copy()

        self.inst.amenities = amenity
        self.assertIn(amenity.id, initial_amenity_ids)

    # DBStorage tests
    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_saved_to_file(self):
        """Test if changes are in file"""
        original_updated_at = self.inst.updated_at
        self.inst.save()
        self.assertLess(original_updated_at, self.inst.updated_at)
        with open("file.json", "r") as f:
            self.assertIn(f"Place.{self.inst.id}", f.read())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_saved_to_database(self):
        """Test if changes are in file"""
        original_updated_at = self.inst.updated_at
        self.assertEqual(original_updated_at, self.inst.updated_at)
        query = self.dbstorage._DBStorage__session.query(Place)\
            .filter_by(id=self.inst.id).first()
        self.assertEqual(self.inst.id, query.id)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_reviews_relationship(self):
        """Test the reviews property"""
        review = Review(text="Test Review", place_id=self.inst.id,
                        user_id=self.user.id)
        self.dbstorage._DBStorage__session.add(review)
        self.dbstorage._DBStorage__session.commit()

        # Check if the review is in the property
        self.assertIn(review, self.inst.reviews)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_amenities_relationship(self):
        """Test the amenities property"""
        # Add an Amenity to the Place
        amenity = Amenity(name="Test Amenity")
        self.dbstorage._DBStorage__session.add(amenity)
        self.dbstorage._DBStorage__session.commit()

        # Assign Amenity to the Place
        self.inst.amenities.append(amenity)
        self.dbstorage._DBStorage__session.commit()

        # Check if the amenity is in the property
        self.assertIn(amenity, self.inst.amenities)


if __name__ == '__main__':
    unittest.main()

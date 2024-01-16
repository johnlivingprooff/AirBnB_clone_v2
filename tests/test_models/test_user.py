#!/usr/bin/python3
"""Unit test for User"""
import unittest
import models
import pep8
import os
import json
from unittest.mock import patch, mock_open
from datetime import datetime
from models.user import User
from models.base_model import BaseModel, Base
from models.place import Place
from models.state import State
from models.city import City
from models.review import Review
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
FileStorage = models.FileStorage
DBStorage = models.DBStorage


class TestUser_pep8(unittest.TestCase):
    """Unittest for State class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertIsNotNone(User.__doc__)

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/user.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestUser(unittest.TestCase):
    """Unittest for User class"""

    # For test_reload method
    read_data = {
        "BaseModel.1": {
            "__class__": "BaseModel",
            "id": "1",
            }
        }

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
        cls.user = User(
            email="test@example.com",
            password="test_password",
            first_name="John",
            last_name="Doe"
        )
        cls.inst = User()

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

        del cls.inst
        del cls.filestorage

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_init(self):
        """Test instantisation"""
        self.assertIsInstance(self.inst, User)

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
        self.assertEqual(User.__tablename__, 'users')

    def test_BaseModel_subclass(self):
        """test if object is an instance of BaseModel"""
        self.assertIsInstance(self.inst, BaseModel)

    def test_class_instance(self):
        """test if object is an instance of BaseModel & Amenity"""
        self.assertIsInstance(self.inst, User)

    def test_str_representation(self):
        """Test the __str__ method"""
        dic = self.inst.__dict__.copy()
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        expected_str = f"[User] ({self.inst.id}) {dic}"
        self.assertEqual(str(self.inst), expected_str)

    def test_multiple_instances(self):
        """Test the behavior of multiple instances"""
        obj = User(text="newText")
        self.assertNotEqual(self.inst, obj)

    def test_unique_models(self):
        """Test checks that two models are unique"""
        model_two = User()
        self.assertNotEqual(model_two.id, self.inst.id)
        self.assertLess(self.inst.created_at, model_two.created_at)
        self.assertNotEqual(model_two.updated_at, self.inst.updated_at)

    def test_user_creation(self):
        # Test creating a User instance
        user = User(email='test@example.com', password='password')

        self.assertIsInstance(user, User)
        self.assertIsInstance(user, BaseModel)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.password, 'password')

    def test_with_args_id(self):
        """Test with specific args"""
        _id = "7q795"
        obj = User(id=_id)
        self.assertEqual(obj.id, _id)

    def test_with_args_created_at(self):
        """Test with specific created at time"""
        _created_at = "2023-12-07T09:49:07.936066"
        d_format = "%Y-%m-%dT%H:%M:%S.%f"
        obj_c_at = datetime.strptime(_created_at, d_format)
        obj = User(created_at=_created_at)
        self.assertEqual(obj.created_at, obj_c_at)

    def test_with_args_updated_at(self):
        """Test with specific updated at time"""
        _updated_at = "2023-12-07T09:49:07.936066"
        d_format = "%Y-%m-%dT%H:%M:%S.%f"
        obj_u_at = datetime.strptime(_updated_at, d_format)
        obj = User(created_at=_updated_at)
        self.assertEqual(obj.created_at, obj_u_at)

    def test_with_args_email(self):
        """Test with specific email"""
        _var = "youremail@mail.com"
        obj = User(email=_var)
        self.assertEqual(obj.email, _var)

    def test_with_args_password(self):
        """Test with specific password"""
        _var = "456gfg8*$#"
        obj = User(password=_var)
        self.assertEqual(obj.password, _var)

    def test_with_args_first_name(self):
        """Test with specific first name"""
        _var = "MyName"
        obj = User(first_name=_var)
        self.assertEqual(obj.first_name, _var)

    def test_with_args_first_name(self):
        """Test with specific last name"""
        _var = "surnName"
        obj = User(last_name=_var)
        self.assertEqual(obj.last_name, _var)

    def test_empty_email(self):
        """Test if the class handles empty email"""
        user = User(email='')
        self.assertEqual(user.email, '')

    def test_none_password(self):
        """Test if the class handles None password"""
        user = User(password=None)
        self.assertIsNone(user.password)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_user_relationship_with_place_and_review(self):
        """Test the relationship between User, Place, and Review"""
        place = self.place
        review = Review(text='TestReview', user_id=self.user.id,
                        place_id=place.id)
        user = self.user
        user.places.append(place)
        user.reviews.append(review)

        self.dbstorage._DBStorage__session.add(review)
        self.dbstorage._DBStorage__session.commit()

        # Check if the places attribute is working
        self.assertIsInstance(user.places, list)
        self.assertEqual(len(user.places), 1)
        self.assertEqual(user.places[0], place)

        # Check if the reviews attribute is working
        self.assertIsInstance(user.reviews, list)
        self.assertEqual(len(user.reviews), 1)
        self.assertEqual(user.reviews[0], review)

        # Check if the backrefs are set on the Place and Review sides
        self.assertEqual(place.user, user)
        self.assertEqual(review.user, user)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_user_relationships(self):
        """Test the relationships with Place and Review"""
        # Create a Place and a Review related to the User
        place = Place(name="Test Place", user_id=self.user.id,
                      city_id=self.city.id)
        review = Review(text="Test Review", user_id=self.user.id,
                        place_id=place.id)

        self.dbstorage._DBStorage__session.add(place)
        self.dbstorage._DBStorage__session.add(review)
        self.dbstorage._DBStorage__session.commit()

        # Query the User and check if the relationships are correct
        queried_user = self.dbstorage._DBStorage__session.query(User)\
            .filter_by(email="test").first()
        self.assertTrue(place in queried_user.places)
        self.assertTrue(review in queried_user.reviews)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing DBStorage")
    @patch(
            "builtins.open", new_callable=mock_open,
            read_data=json.dumps(read_data)
            )
    def test_reload(self, mock_open_file):
        """Test the reload method, whether objects
        are correctly deserialized from a JSON file
        """
        models.storage.reload()
        obj = BaseModel()
        obj.id = "1"
        key = f"BaseModel.{obj.id}"
        self.assertEqual(models.storage.all()[key].id, obj.id)


if __name__ == '__main__':
    unittest.main()

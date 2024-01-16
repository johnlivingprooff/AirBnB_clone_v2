#!/usr/bin/python3
"""Unit test for Review"""
import os
import unittest
import models
import MySQLdb
import pep8
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import OperationalError
from unittest.mock import patch
from models.base_model import Base, BaseModel
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from models.place import Place
from models.review import Review
FileStorage = models.FileStorage
DBStorage = models.DBStorage


class TestReview_pep8(unittest.TestCase):
    """Unittest for Review class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertIsNotNone(Review.__doc__)

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/review.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestReview(unittest.TestCase):
    """Unittest for Review class"""

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
        cls.inst = Review(text="Test Review")
        cls.user = User(name="Test User")
        cls.place = Place(name="Test Place")

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

            cls.inst = Review(text="Test Review", place_id=cls.place.id,
                              user_id=cls.user.id)
            cls.dbstorage._DBStorage__session.add(cls.inst)
            cls.dbstorage._DBStorage__session.commit()

    def tearDown(cls):
        """Clean up after each test"""
        try:
            os.remove("file.json")
        except IOError:
            pass

        try:
            # restore the original file.json
            os.rename("org_file", "file.json")
        except IOError:
            pass

        # del cls.inst
        # del cls.filestorage

        if os.getenv('HBNB_TYPE_STORAGE') == 'db':
            cls.dbstorage._DBStorage__session.close()

    def test_init(self):
        """Test instantisation"""
        self.assertIsInstance(self.inst, Review)

    def test_core_hasattr(self):
        """Test checks for core attributes"""
        self.assertTrue(hasattr(self.inst, 'id'))
        self.assertTrue(hasattr(self.inst, 'created_at'))
        self.assertTrue(hasattr(self.inst, 'updated_at'))

    def test_text(self):
        """checks for text class attribute"""
        self.assertEqual(self.inst.text, "Test Review")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing DBStorage")
    def test_user_id(self):
        """checks for user id class attribute"""
        self.assertEqual(self.inst.place_id, "")
        self.assertEqual(self.inst.user_id, "")
        self.assertEqual(type(self.inst.text), str)
        self.assertEqual(type(self.inst.place_id), str)
        self.assertEqual(type(self.inst.user_id), str)

    def test_BaseModel_subclass(self):
        """test if object is an instance of BaseModel"""
        self.assertIsInstance(self.inst, BaseModel)

    def test_class_instance(self):
        """test if object is an instance of BaseModel & Amenity"""
        self.assertIsInstance(self.inst, Review)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing DBStorage")
    def test_str_representation(self):
        """Test the __str__ method"""
        dic = self.inst.__dict__.copy()
        if "_sa_instance_state" in dic:
            del dic["_sa_instance_state"]
        expected_str = f"[Review] ({self.inst.id}) {dic}"
        self.assertEqual(str(self.inst), expected_str)

    def test_multiple_instances(self):
        """Test the behavior of multiple instances"""
        obj = Review(text="newText")
        self.assertNotEqual(self.inst, obj)

    def test_unique_models(self):
        """Test checks that two models are unique"""
        model_two = Review()
        self.assertNotEqual(model_two.id, self.inst.id)
        self.assertNotEqual(model_two.updated_at, self.inst.updated_at)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_review_relationships(self):
        """Test the relationships with Place and User"""
        # Query the Review and check if Place and User are in the relationship
        queried_review = self.dbstorage._DBStorage__session.query(Review)\
            .filter_by(text="Test Review").first()
        self.assertEqual(self.place, queried_review.place)
        self.assertEqual(self.user, queried_review.user)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_review_relationship_with_place_and_user(self):
        # Test the relationship between Review, Place, and User
        place = self.place
        user = self.user
        review = self.inst

        self.dbstorage._DBStorage__session.add_all([place, user, review])
        self.dbstorage._DBStorage__session.commit()

        # Check if the place attribute is working
        self.assertEqual(review.place_id, place.id)

        # Check if the user attribute is working
        self.assertEqual(review.user_id, user.id)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_review_table_name(self):
        # Test the table name of the Review class
        self.assertEqual(Review.__tablename__, 'reviews')

    # FileStorage Tests
    @patch('models.storage.save')
    def test_save_method_updates_storage(self, mock_save):
        """Test whether models.storage.save
        is called and updates the storage
        """
        review = Review()
        original_updated_at = review.updated_at
        review.name = 'NewReviewName'
        review.save()
        mock_save.assert_called_once()
        self.assertNotEqual(original_updated_at, review.updated_at)

    @patch('models.storage.all')
    def test_all_method_returns_dict(self, mock_all):
        """Test whether models.storage.all returns a dictionary"""
        mock_all.return_value = {'some_key': 'some_value'}
        result = models.storage.all()
        self.assertIsInstance(result, dict)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage")
    def test_nullable_attributes(self):
        """Test that email attribute is non-nullable."""
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(Review(
                place_id=self.place.id, user_id=self.user.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(Review(
                text="a", user_id=self.user.id))
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises((IntegrityError, OperationalError)):
            self.dbstorage._DBStorage__session.add(Review(
                text="a", place_id=self.place.id))
            self.dbstorage._DBStorage__session.commit()


if __name__ == '__main__':
    unittest.main()

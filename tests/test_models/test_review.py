#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.review import Review
from models.base_model import BaseModel, Base
from models.user import User
from models.place import Place
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv


class test_review(test_basemodel):
    """ """

    @classmethod
    def setUpClass(cls):
        # Create an SQLite database in memory for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(bind=cls.engine)
        Session = sessionmaker(bind=cls.engine)
        cls.session = Session()

    @classmethod
    def tearDownClass(cls):
        # Close the session and clean up the database
        cls.session.close()
        Base.metadata.drop_all(bind=cls.engine)

    def test_review_creation(self):
        # Test creating a Review instance
        review = Review(text='TestReview')

        self.assertIsInstance(review, Review)
        self.assertIsInstance(review, BaseModel)
        self.assertEqual(review.text, 'TestReview')

    def test_review_relationship_with_place_and_user(self):
        # Test the relationship between Review, Place, and User
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            place = Place(name='TestPlace')
            user = User(name='TestUser')
            review = Review(text='TestReview', place=place, user=user)

            self.session.add_all([place, user, review])
            self.session.commit()

            # Check if the place attribute is working
            self.assertEqual(review.place, place)

            # Check if the user attribute is working
            self.assertEqual(review.user, user)

    def test_review_table_name(self):
        # Test the table name of the Review class
        self.assertEqual(Review.__tablename__, 'reviews')

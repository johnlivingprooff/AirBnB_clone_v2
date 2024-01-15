#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review
from os import getenv


class test_User(test_basemodel):
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

    def test_user_creation(self):
        # Test creating a User instance
        user = User(email='test@example.com', password='password')

        self.assertIsInstance(user, User)
        self.assertIsInstance(user, BaseModel)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.password, 'password')

    def test_user_relationship_with_place_and_review(self):
        # Test the relationship between User, Place, and Review
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            place = Place(name='TestPlace')
            review = Review(text='TestReview')
            user = User(email='test@example.com',
                        password='password', places=[place],
                        reviews=[review])

            self.session.add_all([place, review, user])
            self.session.commit()

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

    def test_user_table_name(self):
        # Test the table name of the User class
        self.assertEqual(User.__tablename__, 'users')

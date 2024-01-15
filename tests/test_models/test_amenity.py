#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.place import Place
from models.review import Review
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv


class test_Amenity(test_basemodel):
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

    def test_amenity_creation(self):
        # Test creating an Amenity instance
        amenity = Amenity(name="TestAmenity")
        self.assertIsInstance(amenity, Amenity)
        self.assertIsInstance(amenity, BaseModel)
        self.assertEqual(amenity.name, 'TestAmenity')

    def test_amenity_table_name(self):
        # Test the table name of the Amenity class
        self.assertEqual(Amenity.__tablename__, 'amenities')

    def test_amenity_relationship_with_place(self):
        # Test the relationship between Amenity and Place
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            place = Place(name='TestPlace')
            self.session.add_all([self.amenity, place])
            self.session.commit()
            place.amenities.append(self.amenity)
            self.session.commit()

            # Check if the backref is set on the Place side
            self.assertIn(self.amenity, place.amenities)

    def test_amenity_relationship_with_review(self):
        # Test the relationship between Amenity and Review
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            review = Review(text='TestReview')
            self.session.add_all([self.amenity, review])
            self.session.commit()
            review.amenities.append(self.amenity)
            self.session.commit()

            # Check if the backref is set on the Review side
            self.assertIn(self.amenity, review.amenities)

    def test_amenity_relationship_with_user(self):
        # Test the relationship between Amenity and User
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            user = User(email='test@example.com', password='password')
            self.session.add_all([self.amenity, user])
            self.session.commit()
            user.amenities.append(self.amenity)
            self.session.commit()

            # Check if the backref is set on the User side
            self.assertIn(self.amenity, user.amenities)

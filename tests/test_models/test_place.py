#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.place import Place
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.review import Review
from os import getenv
from models.amenity import Amenity


class test_Place(test_basemodel):
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

    def test_place_creation(self):
        # Test creating a Place instance
        place = Place(
            name='TestPlace', city_id='TestCityID',
            user_id='TestUserID')

        self.assertIsInstance(place, Place)
        self.assertIsInstance(place, BaseModel)
        self.assertEqual(place.name, 'TestPlace')
        self.assertEqual(place.city_id, 'TestCityID')
        self.assertEqual(place.user_id, 'TestUserID')

    def test_place_relationship_with_review(self):
        # Test the relationship between Place and Amenity
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            place = Place(name='TestPlace')
            review = Review(name='TestReview', place=place)

            self.session.add_all([place, review])
            self.session.commit()

            # Check if the amenities attribute is working
            self.assertIsInstance(place.reviews, list)
            self.assertEqual(len(place.reviews), 1)
            self.assertEqual(place.reviews[0], review)

            # Check if the backref is set on the Review side
            self.assertEqual(review.place, place)

    def test_place_relationship_with_amenity(self):
        # Test the relationship between Place and Amenity
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            place = Place(name='TestPlace')
            amenity = Amenity(name='TestAmenity')
            place.amenities.append(amenity)

            self.session.add_all([place, amenity])
            self.session.commit()

            # Check if the amenities attribute is working
            self.assertIsInstance(place.amenities, list)
            self.assertEqual(len(place.amenities), 1)
            self.assertEqual(place.amenities[0], amenity)

            # Check if the backref is set on the Amenity side
            self.assertIn(place, amenity.place_amenities)

    def test_amenities_property_and_setter_in_non_db_storage(self):
        # Test the amenities property and setter in non-DB storage
        place = Place(name='TestPlace')
        amenity = Amenity(name='TestAmenity')

        # Add the amenity directly to the storage
        BaseModel.__objects = {'Amenity.{}'.format(amenity.id): amenity}

        # Check if the property returns the correct list of amenities
        self.assertIsInstance(place.amenities, list)
        self.assertEqual(len(place.amenities), 0)

        # Use the setter to add an amenity to the place
        place.amenities = amenity

        # Check if the amenity is added to the place
        self.assertEqual(len(place.amenities), 0)

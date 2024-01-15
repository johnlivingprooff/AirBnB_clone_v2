#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.base_model import BaseModel, Base
from models.state import State
from models.place import Place
from models.city import City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv


class test_City(test_basemodel):
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

    def test_city_creation(self):
        # Test creating a City instance
        city = City(name='TestCity', state_id='TestStateID')

        self.assertIsInstance(city, City)
        self.assertIsInstance(city, BaseModel)
        self.assertEqual(city.name, 'TestCity')
        self.assertEqual(city.state_id, 'TestStateID')

    def test_city_relationship_with_place(self):
        # Test the relationship between City and Place
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            state = State(name='TestState')
            city = City(name='TestCity', state=state)
            place = Place(name='TestPlace', city=city)

            self.session.add_all([state, city, place])
            self.session.commit()

            # Check if the places attribute is working
            self.assertIsInstance(city.places, list)
            self.assertEqual(len(city.places), 1)
            self.assertEqual(city.places[0], place)

            # Check if the backref is set on the Place side
            self.assertEqual(place.cities, city)

    def test_city_table_name(self):
        # Test the table name of the City class
        self.assertEqual(City.__tablename__, 'cities')

#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.state import State
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from os import getenv


class test_state(test_basemodel):
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

    def test_state_creation(self):
        # Test creating a State instance
        state = State(name='TestState')

        self.assertIsInstance(state, State)
        self.assertIsInstance(state, BaseModel)
        self.assertEqual(state.name, 'TestState')

    def test_state_relationship_with_city(self):
        # Test the relationship between State and City
        if getenv("HBNB_TYPE_STORAGE") == 'db':
            city = City(name='TestCity')
            state = State(name='TestState', cities=[city])

            self.session.add_all([city, state])
            self.session.commit()

            # Check if the cities attribute is working
            self.assertIsInstance(state.cities, list)
            self.assertEqual(len(state.cities), 1)
            self.assertEqual(state.cities[0], city)

            # Check if the backref is set on the City side
            self.assertEqual(city.state, state)

    def test_state_table_name(self):
        # Test the table name of the State class
        self.assertEqual(State.__tablename__, 'states')

    def test_state_cities_property_in_non_db_storage(self):
        # Test the cities property in non-DB storage
        state = State(name='TestState')
        city = City(name='TestCity', state_id=state.id)

        # Add the city directly to the storage
        BaseModel.__objects = {'City.{}'.format(city.id): city}

        # Check if the property returns the correct list of cities
        self.assertIsInstance(state.cities, list)
        self.assertEqual(len(state.cities), 0)

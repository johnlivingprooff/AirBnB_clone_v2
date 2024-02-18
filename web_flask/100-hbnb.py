#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, abort, render_template
from models import storage
from models.state import State
from models.amenity import Amenity
from models.place import Place


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ displays the states, cities & amenities """
    states = storage.all(State).values()
    amenities = storage.all(Amenity).values()
    places = storage.all(Place).values()

    return render_template('100-hbnb.html',
                           states=states, amenities=amenities,
                           places=places)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

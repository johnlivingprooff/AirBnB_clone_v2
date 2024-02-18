#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, abort, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown(exception):
    """ Remove the current SQLAlchemy Session """
    storage.close()


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    """ displays a list of the cities by states """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)

    return render_template('8-cities_by_states.html', states=sorted_states)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

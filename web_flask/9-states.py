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


@app.route('/states', strict_slashes=False, defaults={'id': None})
@app.route('/states/<id>', strict_slashes=False)
def state_cities(id):
    """ displace the cities of a state id """
    states = storage.all(State).values()
    sorted_states = sorted(states, key=lambda x: x.name)
    if id is None:
        return render_template('7-states_list.html', states=sorted_states)

    for state in sorted_states:
        if state.id == id:
            return render_template('9-states.html', state=state)

    return render_template('9-states.html', state=None)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

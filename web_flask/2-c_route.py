#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello():
    """ displays Hello HBNB! """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ displays HBNB """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):
    """ displays C with <text> variable """
    withSpace = text.replace('_', ' ')
    return f"C {withSpace}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

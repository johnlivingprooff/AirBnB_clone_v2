#!/usr/bin/python3
"""starts a Flask web application"""
from flask import Flask, abort, render_template


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


@app.route('/python/', defaults={'text': 'is cool'}, strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def py_text(text):
    """ displays Python with <text> variable """

    withSpace = text.replace('_', ' ')
    return f"Python {withSpace}"


@app.route('/number/<n>', strict_slashes=False)
def number(n):
    """ display “n is a number” only if n is an integer """

    try:
        n = int(n)
        return f"{n} is a number"
    except Exception:
        abort(404)


@app.route('/number_template/<int:n>', strict_slashes=False)
def number_temp(n):
    """ Renders an HTML file only if n is an integer """

    return render_template('5-number.html', number=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def number_odd_or_even(n):
    """ Renders an HTML file only if n is an integer """
    if n % 2 == 0:
        odd_even = "even"
    else:
        odd_even = "odd"

    return render_template('6-number_odd_or_even.html', number=n, odd_even=odd_even)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

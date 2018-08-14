from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME']='todoapp'
app.config['MONGO_URI']='mongodb://todoapp:pass123@ds219832.mlab.com:19832/todoapp'
mongo = PyMongo(app)

@app.route("/")
def index():
    # load interface here
    return 'Hello World'


@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    app.run(debug = True)
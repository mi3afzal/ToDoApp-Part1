from flask import Flask, render_template, url_for, request, jsonify, redirect, session
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['MONGO_DBNAME']='todoapp'
app.config['MONGO_URI']='mongodb://todoapp:pass123@ds219832.mlab.com:19832/todoapp'
mongo = PyMongo(app)


app.run(debug = True)
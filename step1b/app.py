from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['MONGO_DBNAME'] = 'todoapp'
app.config['MONGO_URI'] = 'mongodb://todoapp:pass123@ds219832.mlab.com:19832/todoapp'
mongo = PyMongo(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://srbxlsob:s8cSQ4U_nm7vaXL9hW9QZLHxq-0R6wlp@horton.elephantsql.com:5432/srbxlsob'
db = SQLAlchemy(app)


# Create our database model
class Tasks(db.Model):
    __tablename__ = "tasks"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    done = db.Column(db.Boolean, default=False)

    def __init__(self, title, description, done=False):
        self.title = title
        self.description = description
        self.done = done

    def __repr__(self):
        return '<id {}>'.format(self.id)


@app.route("/")
def index():
    # load interface here
    return 'To Do App Interface'


@app.route("/todo/api/v1.0/tasks", methods = ['GET'])
def get_all_tasks():
    data = []
    db_task = Tasks.query.all()
    if db_task:
        for task in db_task:
            data.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "done": task.done
            })
    return jsonify({'tasks':data})


@app.route("/todo/api/v1.0/tasks/<task_id>", methods = ['GET'])
def get_task(task_id):
    data = []
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        data.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "done": task.done
        })
    else:
        response = {'status': 'error', 'status_code': '404', 'message': 'Task not Found'}
    return jsonify({'tasks':data})


@app.route("/todo/api/v1.0/tasks", methods = ['POST'])
def create_tasks():
    title = request.json.get("title", '')
    description = request.json.get('description', '')

    task = Tasks(title, description)
    db.session.add(task)
    db.session.commit()

    return jsonify({"id": task.id})


@app.route("/todo/api/v1.0/tasks/<task_id>", methods=['PUT'])
def update_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        task.title = request.json.get("title", task.title)
        task.description = request.json.get('description', task.description)
        task.done = bool(request.json.get("done", task.done))
        db.session.commit()
        response = {'status': 'success', 'status_code': '200', 'message': 'Task Updated'}
    else:
        response = {'status': 'error', 'status_code': '404', 'message': 'Task not Found'}
    return jsonify({'response': response})


@app.route("/todo/api/v1.0/tasks/<task_id>", methods = ['DELETE'])
def delete_task(task_id):
    task = Tasks.query.filter_by(id=task_id).first()
    if task:
        db.session.delete(task)
        db.session.commit()
        response = {'status': 'success', 'status_code': '200', 'message': 'Task Deleted'}
    else:
        response = {'status': 'error', 'status_code': '404', 'message': 'Task not Found'}
    return jsonify({'response': response})


@app.errorhandler(404)
def not_found_error(e):
    response = {'status': 'error', 'status_code': '404', 'message': 'Task not Found'}
    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug = True)
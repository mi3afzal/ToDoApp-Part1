from flask import Flask, request, jsonify, json
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_DBNAME']='todoapp'
app.config['MONGO_URI']='mongodb://todoapp:pass123@ds219832.mlab.com:19832/todoapp'
mongo = PyMongo(app)

@app.route("/")
def index():
    # load interface here
    return 'To Do App Interface'


@app.route("/todo/api/v1.0/tasks", methods = ['GET'])
def get_all_tasks():
    data = []
    db_task = mongo.db.tasks.find()
    if db_task.count() > 0:
        for task in db_task:
            data.append({"id": str(task["_id"]), "title": task["title"], "description": task["description"], "done": task["done"]})
    return jsonify({'tasks':data})


@app.route("/todo/api/v1.0/tasks/<task_id>", methods = ['GET'])
def get_task(task_id):
    data = []
    db_task = mongo.db.tasks.find({"_id": ObjectId(task_id)})
    if db_task.count() > 0:
        for task in db_task:
            data.append({"id": str(task["_id"]), "title": task["title"], "description": task["description"], "done": task["done"]})
    return jsonify({'tasks':data})


@app.route("/todo/api/v1.0/tasks", methods = ['POST'])
def create_tasks():
    title = request.json["title"]
    description = request.json['description']

    db_task = mongo.db.tasks
    new_task_id = db_task.insert({"title": title, "description": description, "done": False}) # bool()
    return jsonify({"id": str(new_task_id)})


@app.route("/todo/api/v1.0/tasks/<task_id>", methods = ['PUT'])
def update_task(task_id):
    db_task = mongo.db.tasks
    task = db_task.find_one({"_id": ObjectId(task_id)})
    if db_task != '':
        title = request.json.get("title", task["title"])
        description = request.json.get('description', task["description"])
        done = bool(request.json.get("done", task["done"]))

        task["title"] = title
        task["description"] = description
        task["done"] = done
        db_task.save(task)
        response = {'status': 'success', 'status_code': '200', 'message': 'Task Updated'}
    else:
        response = {'status': 'error', 'status_code': '404', 'message': 'Task not Found'}

    return jsonify({'response': response})


@app.route("/todo/api/v1.0/tasks/<task_id>", methods = ['DELETE'])
def delete_task(task_id):
    db_response = mongo.db.tasks.delete_one({"_id": ObjectId(task_id)})
    response = {'status': 'success', 'status_code': '200', 'message': 'Task Deleted'}
    return jsonify({'response': response})


if __name__ == "__main__":
    app.run(debug = True)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://osama:123456@localhost:5432/taskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)


@app.route("/", methods=['GET'])
def index():
    tasks = Task.query.order_by(Task.id).all()
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=['POST'])
def add():
    task_name = request.form.get("task")
    if task_name:
        new_task = Task(name = task_name)
        db.session.add(new_task)
        db.session.commit()
    return redirect("/")


@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return {"error": "Task not found"}, 404
    
    db.session.delete(task)
    db.session.commit()
    return {"message": "Deleted"}


@app.route("/tasks/<int:task_id>/edit", methods=['GET'])
def edit_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return "Task not found", 404
    
    return render_template("edit.html", task=task)


@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = Task.query.get(task_id)

    if not task:
        return {"error": "Task not found"}, 404
    
    task.name = data["name"]
    db.session.commit()

    
    return {"message": "Updated", "task": task}


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
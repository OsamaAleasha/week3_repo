from flask import Flask, render_template, request, redirect, url_for, jsonify

app = Flask(__name__)

tasks = []
task_id_counter = 1


@app.route("/", methods=['GET'])
def index():
    return render_template("index.html", tasks=tasks)



@app.route("/add", methods=['POST'])
def add():
    global task_id_counter
    task_name = request.form.get("task")
    if task_name:
        tasks.append({"id": task_id_counter, "name": task_name})
        task_id_counter += 1
    return redirect("/")



@app.route("/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return {"error": "Task not found"}, 404
    tasks.remove(task)
    return {"message": "Deleted"}



@app.route("/tasks/<int:task_id>/edit", methods=['GET'])
def edit_task(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return "Task not found", 404
    return render_template("edit.html", task=task)


@app.route("/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    if not data or "name" not in data:
        return {"error": "Invalid request"}, 400

    task = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return {"error": "Task not found"}, 404

    task["name"] = data["name"]
    return {"message": "Updated", "task": task}


if __name__ == "__main__":
    app.run(debug=True)
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
load_dotenv()

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
parser = StrOutputParser()

summarize_prompt = PromptTemplate.from_template(
    "Summarize these tasks briefly in one sentence:\n{tasks}"
)

classify_prompt = PromptTemplate.from_template(
    "Classify each task strictly into ONE category only: Work, Study, or Personal.\n\nTasks:\n{summary}"
)

priority_prompt = PromptTemplate.from_template(
    "Based on this summary:\n{summary}\n\n"
    "And these categories:\n{categories}\n\n"
    "Give only a simple list of tasks with their priority (High, Medium, Low)."
) 


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


@app.route("/ai-plan")
def ai_plan():
    tasks = Task.query.all()

    if not tasks:
        return render_template("ai.html", summary="", categories="", priority="")

    task_text = "\n".join([t.name for t in tasks])

    summary = (summarize_prompt | llm | parser).invoke({"tasks": task_text})
    categories = (classify_prompt | llm | parser).invoke({"summary": summary})
    priority = (priority_prompt | llm | parser).invoke({
        "summary": summary,
        "categories": categories
    })

    return render_template("ai.html",
                           summary=summary,
                           categories=categories,
                           priority=priority)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
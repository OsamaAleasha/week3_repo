from flask import Flask, render_template, request
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = Flask(__name__)

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3
)

parser = StrOutputParser()


summarize_prompt = PromptTemplate.from_template(
    "Summarize these tasks briefly in one sentence:\n{tasks}"
)

classify_prompt = PromptTemplate.from_template(
    "Based on this summary, classify each task strictly into ONE category only: Work, Study, or Personal.\n\nSummary:\n{summary}"
)


priority_prompt = PromptTemplate.from_template(
    "Based on this summary:\n{summary}\n\n"
    "And these categories:\n{categories}\n\n"
    "Give only a simple list of tasks with their priority (High, Medium, Low)."
)

@app.route("/", methods=["GET", "POST"])
def home():
    summary = ""
    categories = ""
    priority = ""
    original_tasks = ""

    if request.method == "POST":
        original_tasks = request.form["tasks"]

        summary = (summarize_prompt | llm | parser).invoke({"tasks": original_tasks})
        categories = (classify_prompt | llm | parser).invoke({"summary": summary})
        priority = (priority_prompt | llm | parser).invoke({
            "summary": summary,
            "categories": categories
        })

    return render_template(
        "index.html",
        tasks=original_tasks,
        summary=summary,
        categories=categories,
        priority=priority
    )

if __name__ == "__main__":
    app.run(debug=True)
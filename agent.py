from langchain_core.tools import Tool
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

def count_words(text: str) -> str:
    return f"Number of words: {len(text.split())}"

def summarize(text: str) -> str:
    return "Summary: The day consisted of a workout, 8 hours of work, and cooking a healthy meal."

tools = [
    Tool(name="word_counter", func=count_words, description="Counts words in a string"),
    Tool(name="summarizer", func=summarize, description="Summarizes daily tasks")
]

llm = ChatOpenAI(model="gpt-4o-mini")
agent = create_agent(llm, tools=tools)

user_input = input("Enter your task:\n")


result = agent.invoke({
    "messages": [{"role": "user", "content": user_input}]
})

print("\nAgent Result:")
print(result["messages"][-1].content)
from flask import Flask, render_template, request
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel 
from dotenv import load_dotenv
from Sequential import run_ai

import os

load_dotenv()

app = Flask(__name__)

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

summarize_prompt = PromptTemplate.from_template(
    "Summarize these tasks in one single sentence. "
    "Do not include any introductory phrases: {tasks}"
)

classify_prompt = PromptTemplate.from_template(
    "Categorize the following tasks into Work and Personal groups. "
    "Instructions: Do not use any bolding or asterisks (**). "
    "Do not say 'Sure' or 'Here are your tasks'. "
    "Format as 'Category Name:' followed by the list.\nTasks:\n{tasks}"
)

priority_prompt = PromptTemplate.from_template(
    "Assign High, Medium, or Low priority to these tasks. "
    "Instructions: Do not use bolding or asterisks (**). "
    "Provide only the list of tasks with their priority level. "
    "No conversational filler or introductory text.\nTasks:\n{tasks}"
)

chain = RunnableParallel({
    "summary": summarize_prompt | llm | StrOutputParser(),
    "categories": classify_prompt | llm | StrOutputParser(),
    "priority": priority_prompt | llm | StrOutputParser()
})

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    original_tasks = ""
    if request.method == "POST":
        original_tasks = request.form.get("tasks")
        if original_tasks:
           
            result = chain.invoke({"tasks": original_tasks})
    
    return render_template("index.html", result=result, original_tasks=original_tasks)

if __name__ == "__main__":
    app.run(debug=True)
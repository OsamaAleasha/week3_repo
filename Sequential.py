from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel 
from dotenv import load_dotenv
import os

load_dotenv()
llm = ChatOpenAI(model="gpt-4o-mini")

summarize_prompt = PromptTemplate.from_template(
    "Summarize the general nature of these tasks in one sentence: {tasks}"
)

classify_prompt = PromptTemplate.from_template(
    "Separate these tasks into 'Work' and 'Personal' categories:\n{tasks}"
)

priority_prompt = PromptTemplate.from_template(
    "Assign a priority (High, Medium, Low) to each of these tasks: {tasks}"
)

chain = RunnableParallel({
    "summary": summarize_prompt | llm | StrOutputParser(),
    "categories": classify_prompt | llm | StrOutputParser(),
    "priority": priority_prompt | llm | StrOutputParser()
})

def run_ai(tasks):
    result=chain.invoke({"tasks": tasks})
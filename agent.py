#----Importing-----
from langchain_openrouter import ChatOpenRouter
from langchain_openai import ChatOpenAI
from langchain.messages import SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate, MessagesPlaceholder
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.runnables import RunnableSequence

import os


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

model = ChatOpenRouter(
    model="nvidia/nemotron-3-nano-30b-a3b:free",
    api_key=OPENROUTER_API_KEY
)




tasks = """- Finish report 
- Prepare slides 
- Buy groceries
-Schedule meeting
- Reply to emails"""

sum_prompt = ChatPromptTemplate.from_template("""Summarize these tasks in one sentence: {input_text}""")
categ_prompt = ChatPromptTemplate.from_template("""Categorize these tasks into Work and Personal: {summary}""")
prior_prompt = ChatPromptTemplate.from_template("""Prioritize these tasks into High, Medium, and Low {categories}""")


sum_chain = sum_prompt | model
categ_chain = categ_prompt | model
prior_chain = prior_prompt | model

summary = sum_chain.invoke({"input_text": tasks}).content
categories = categ_chain.invoke({"summary": summary}).content
priorities = prior_chain.invoke({"categories":categories}).content

print(" Summary")
print(summary)
print("\n Categories")
print(categories)
print("\n Priorities")
print(priorities)

# @tool
# def sum_file() -> str:
#     """Reads the text file and returns its full content so it can be summarized"""

#     with open(file_path, "r") as f:
#         return f.read()

# #------------------------------------

# @tool
# def word_count(word: str) -> str:
#     """Counts how many times a specific word appears in the text file."

#     Args:
#         word: The word to search for (case-insensitive).
#     """
#     with open(file_path) as file:
#         content = file.read()

#     count = content.lower().split().count(word.lower())
#     return f"The word {word} appears {count} times."

# agent = create_agent(model = model, tools=[sum_file, word_count], system_prompt=prompt)

# response_file = agent.invoke({
    
#     "messages": [{"role":"user", "content":"Summarize the text file given."}],
#     "file_path":file_path
# })
# print(response_file["messages"][-1].content)

# response_count = agent.invoke({
#     "messages": [{"role":"user", "content":"How many times does the word 'mara' appeared in the text file?"}],
#     "file_path":file_path
# })
# print("--------------------------------------")
# print(response_count["messages"][-1].content)




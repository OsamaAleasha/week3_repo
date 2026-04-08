from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage

load_dotenv()

@tool
def Summarizer(text: str) -> str:
    """Summarizes text."""
    return f"Summary: {text[:50]}..."

@tool
def WordCounter(text: str) -> str:
    """Counts words."""
    return f"Word count: {len(text.split())}"

# Setup
agent = create_agent(ChatOpenAI(model="gpt-4o-mini"), [Summarizer, WordCounter])

# Execution
text = "Summarize and count: This is a test for the new LangChain v1 agent."
result = agent.invoke({"messages": [HumanMessage(content=text)]})

# Print the last message in the conversation (the answer)
print(result["messages"][-1].content)
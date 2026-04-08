import os 
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
prompt = PromptTemplate(
   input_variables=["task"],
   template="Give a clear plan to accomplish this task: {task}"
  )

llm = ChatOpenAI(
   model="gpt-4o-mini",
   temperature=0.3,
   api_key=api_key
   )


prompt_text = prompt.format(task="Finish my university assignment")

result = llm.invoke(prompt_text)

print(result.content)
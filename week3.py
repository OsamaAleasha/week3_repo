from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate

import os 


load_dotenv()
key = os.getenv("OPENAI_API_KEY")




llm = ChatOpenAI(
  
    model="gpt-4o-mini"

)
prompt=PromptTemplate(
    input_variables=["task"],
    template="Simmarize the follwing daily task in one short sentence:\n{task}"
)

user_task="clean my room"
final_prompt=prompt.format(task=user_task)
response=llm.invoke(final_prompt)
output=response.content



print("\nTask Summary:")
print(output)
from langchain.llms import OpenAI
from prompts import task_creation_prompt
from langchain.chains import LLMChain

llm = OpenAI(temperature=0.9)
objective = "Grow an autonomous, synthetic intelligence"

chain = LLMChain(llm=llm, prompt=task_creation_prompt)

print(chain.run(objective))
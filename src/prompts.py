from langchain.prompts import PromptTemplate

task_creation_prompt = PromptTemplate(
    input_variables = ["objective"],
    template = "Create a task that will achieve the following objective: {objective}"
)
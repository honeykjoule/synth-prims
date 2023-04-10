from langchain.prompts import PromptTemplate

task_creation_template = """
Create a task that will achieve the following objective: {objective}. 
The last completed task had this result: {result}, based on this description: {description}. 
These are the incomplete tasks: {incomplete_tasks}. 
These are the completed tasks: {completed_tasks}.
"""

task_creation_prompt = PromptTemplate(
    partial_variables=["objective"],
    input_variables = ["result", "description", "incomplete_tasks", "completed_tasks"],
    template = task_creation_template
)

task_prioritization_template = """
Clean, format, and prioritize the following tasks: {task_names}.
Consider the the objective when prioritizing: {objective}.
Do not remove any tasks and return the result as a number list, like
#. Most important task to do next.
#. Second most important task to do next.
Start the task list with number {next_task_list_id}.
"""

task_prioritization_prompt = PromptTemplate(
    partial_variables = ["objective"]
    input_variables = ["task_names", "next_task_list_id"]
    template = task_prioritization_template
)

task_execution_template = """
Complete the following task: {task_name}. Use the task to achieve this objective: {objective}.
Consider the previously completed tasks: {context}.
Task Completion:
"""

task_execution_prompt = PromptTemplate(
    partial_variables=["objective"],
    input_variables = ["task_name", "context"],
    template = task_execution_template
)
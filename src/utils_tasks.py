from utils_json import json_dump, json_load
from utils_openai import get_openai_completion

def initialize_tasks(
    objective,
    initial_task
):
    incomplete_task_list = [{"incomplete task": initial_task, "index": 0}]
    completed_task_list = [{"completed task": None, "index": 0, "result": None}]
    json_data = {
        "objective": objective, 
        "incomplete task list": incomplete_task_list, 
        "completed task list": completed_task_list
    }
    json_dump(json_data, "tasks.json")
    return json_data

# get the objective and task list from the json
def execute_task(
    objective,
    next_task,
    incomplete_task_list,
    completed_task_list
):
    objective = json_load("tasks.json")["objective"]
    # incomplete_task_list = json_load("tasks.json")["incomplete task list"]
    # completed_task_list = json_load("tasks.json")["completed task list"]
    # next_task = incomplete_task_list[0]
    prompt = f"""
    Complete the task: {next_task} to achieve the objective: {objective}.
    This is the list of incompleted tasks: {incomplete_task_list}
    This is the list of completed task: {completed_task_list}"""
    response = get_openai_completion(prompt=prompt)
    #text = response["choices"][0]["text"]
    return response

def create_new_tasks(
    objective,
    result,
    completed_task
):
    prompt = f"""
    Create new tasks to achieve the objective: {objective}.
    The result of the last completed task: {completed_task} is: {result}"""
    response = get_openai_completion(prompt=prompt)
    return response

    

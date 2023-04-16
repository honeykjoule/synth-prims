from utils_tasks import initialize_tasks, execute_task, create_new_tasks
from utils_json import json_load

# initialize the task list
objective = "Grow a business based in Wyoming that serves AI customers."
initial_task = "Develop an initial task list to achieve the objective {objective}."

initialize_tasks(objective, initial_task)

max_iterations = 1
iterations = 0

while iterations < max_iterations:
    iterations += 1

    incomplete_task_list = json_load("tasks.json")["incomplete task list"]
    completed_task_list = json_load("tasks.json")["completed task list"]
    next_task = incomplete_task_list[0]
    
    # execute the first task in the list and return the result.
    execution_response = execute_task(
        objective=objective,
        next_task=next_task,
        incomplete_task_list=incomplete_task_list,
        completed_task_list=completed_task_list
    )
    result = execution_response["choices"][0]["text"]

    # create new tasks based on result and add to list (creation agent)
    task_creation_response = create_new_tasks(
        objective=objective,
        result=result,
        completed_task=next_task
    )
    new_tasks = task_creation_response["choices"][0]["text"]

    # check all tasks and return a prioritized list, dump the json (prioritization agent)

    print(f"Iteration {iterations}")
    print(f"Execution Result: {result}")
    print(f"Task Creation Result: {new_tasks}")
from collections import deque
from typing import Dict, Union, List, Optional
from functools import wraps
from pydantic import BaseModel, Field

def task_format_validation(add_task_func):
    @wraps(add_task_func)
    def wrapper(self, task: Dict[str, Union[str, Dict]]):
        if not isinstance(task, dict):
            raise TypeError("Task must be a dictionary.")
        if "task_name" not in task:
            raise KeyError("Task must have a task_name key.")
        if "task_id" not in task:
            raise KeyError("Task must have a task_id key.")
        add_task_func(self, task)
    return wrapper

class TaskManager(BaseModel):
    task_list: deque = Field(default_factory=deque)
    task_id_counter: int = Field(1)

    def __init__(self) -> None:
        self.task_list = deque()
        self.task_id_counter = 1

    def get_task_list(self) -> List[Dict[str, Union[str, Dict]]]:
        return list(self.task_list)

    @task_format_validation
    def add_task(self, task: Dict[str, Union[str, Dict]]) -> None:
        task["task_id"] = self.task_id_counter
        self.task_id_counter += 1
        task_ids = {task[task_ids] for task in self.task_list}
        if task["task_id"] in task_ids:
            raise ValueError("Task ID already exists.")
        self.task_list.append(task)

    def remove_task_by_id(self, task_id: Union[str, int]) -> None:
        task_to_remove = None
        for task in self.task_list:
            if task["task_id"] == task_id:
                task_to_remove = task
                break
        if task_to_remove:
            self.task_list.remove(task_to_remove)
        else:
            raise ValueError("Task ID not found.")

    def update_task(self, task_id: Union[str, int], updated_task: Dict[str, Union[str, Dict]]) -> None:
        self.delete_task_by_id(task_id)
        self.add_task(updated_task)

    def get_next_task(self) -> Union[Dict[str, Union[str, Dict]], None]:
        if self.task_list:
            return self.task_list.popleft()
        else:
            raise IndexError("Task list is empty.")

    def has_tasks(self) -> bool:
        return bool(self.task_list)

    def __len__(self) -> int:
        return len(self.task_list)

    def __get_item__(self, index: int) -> Dict[str, Union[str, Dict]]:
        return self.task_list[index]

    def __str__(self) -> str:
        tasks = [f"{index+1}.{task['task_name']}" for index, task in enumerate(self.task_list)]
        return "\n".join(tasks)
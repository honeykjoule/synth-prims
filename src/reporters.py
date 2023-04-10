from typing import List, Dict, Union

# Console reporters
def print_colored(text: str, color_code: str) -> None:
    print(f"{color_code}{text}\033[0m")

def print_task_list(task_list: List[Dict[str, Union[str, Dict]]]) -> None:
    print_colored("\n*****TASK LIST*****", "\033[95m\033[1m")
    for task in task_list:
        print(f"{task['task_id']}: {task['task_name']}")
    print_colored("*****END TASK LIST*****", "\033[95m\033[1m")

def print_next_task(task: List[Dict[str, Union[str, Dict]]]) -> None:
    print_colored("\n*****NEXT TASK*****", "\033[92m\033[1m")
    print(f"{task['task_id']}: {task['task_name']}")
    print_colored("*****END NEXT TASK*****", "\033[92m\033[1m")

def print_task_result(result: str) -> None:
    print_colored("\n*****TASK RESULT*****", "\033[93m\033[1m")
    print(result)
    print_colored("*****END TASK RESULT*****", "\033[93m\033[1m")
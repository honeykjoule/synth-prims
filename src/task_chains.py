from prompts import task_creation_prompt, task_prioritization_prompt, task_execution_prompt
from langchain import LLMChain
from langchain.llms import BaseLLM
from pinecone import get_vectorstore
from typing import List, Dict, Union

class TaskCreation(LLMChain):
    @classmethod
    def from_llm(cls, llm: BaseLLM, verbose: bool = True) -> LLMChain:
        return cls(
            prompt=task_creation_prompt,
            llm=llm,
            verbose=verbose,
        )
    def get_next_task(self, result: Dict, task_description: str, task_list: List[str]) -> List[Dict]:
        incomeplete_tasks = ", ".join(task_list)
        response = self.run(result=result, description=task_description, incomplete_tasks=incomeplete_tasks)
        new_tasks = response.split("\n")
        return [{"task_name": task_name} for task_name in new_tasks if task_name.strip()]


class TaskPrioritization(LLMChain):
    @classmethod
    def from_llm(cls, llm: BaseLLM, objective: str, verbose: bool = True) -> LLMChain:
        return cls(
            prompt=task_prioritization_prompt,
            llm=llm,
            verbose=verbose
        )
    def prioritize_tasks(self, this_task_id: int, task_list: List[Dict] -> List[Dict]:
        task_names = [task["task_name"] for task in task_list]
        next_task_id = int(this_task_id) + 1
        response = self.run(task_names=task_names, next_task_id=next_task_id)
        new_tasks = response.split("\n")
        prioritized_tasks = []
        
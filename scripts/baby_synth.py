# https://python.langchain.com/en/latest/modules/chains/examples/baby_agi.html?highlight=baby
# https://github.com/hwchase17/langchain/blob/50c511d75f6f4a5390cfaa97f94a99b58e7eceec/docs/modules/chains/examples/baby_agi.ipynb#L8

import os
from dotenv import load_dotenv
from collections import deque
from typing import Dict, List, Optional
from pydantic import BaseModel, Field

import pinecone
import openai

from langchain import LLMChain, OpenAI, PromptTemplate, BasePromptTemplate
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import BaseLLM
from langchain.vectorstores import Pinecone
from langchain.vectorstores.base import VectorStore

index_name = "baby-synth"
OBJECTIVE = "Grow a synthetic intelligence"
INITIAL_TASK = "Develop a task list"

load_dotenv()

llm = OpenAI()

openai_api_key = os.environ.get("OPENAI_API_KEY")

pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENVIRONMENT"],
)

embeddings_model =  OpenAIEmbeddings()

dimensions = 1536
metric = "cosine"
pod_type = "p1"
if index_name not in pinecone.list_indexes():
    pinecone.create_index(
        name=index_name,
        dimension=dimensions,
        metric=metric,
        pod_type=pod_type,
    )

text_key = "text"
if index_name in pinecone.list_indexes():
    index = pinecone.Index(index_name)
else:
    raise ValueError(f"Index {index_name} not found in your Pinecone project.")

vectorstore = Pinecone(index, embeddings_model.embed_query, text_key)

class TaskCreationChain(LLMChain):

    @classmethod
    def from_llm(cls, llm: BaseLLM, objective: str, verbose: bool = False) -> LLMChain:
        task_creation_template = (
            "You are an task creation AI that uses the result of an execution agent"
            " to create new tasks with the following objective: {objective},"
            " The last completed task has the result: {result}."
            " This result was based on this task description: {task_description}."
            " These are incomplete tasks: {incomplete_tasks}."
            " Based on the result, create new tasks to be completed"
            " by the AI system that do not overlap with incomplete tasks."
            " Return the tasks as an array."
        )
        prompt = PromptTemplate(
            template=task_creation_template,
            # partial_variables={"objective": objective},
            input_variables=["objective", "result", "task_description", "incomplete_tasks"],
        )
        return cls(llm=llm, prompt=prompt, verbose=verbose)

    def get_next_task(self, objective: str, result: Dict, task_description: str, task_list: List[str]):
        incomplete_tasks = ", ".join(task_list)
        response = self.run(objective=objective, result=result, task_description=task_description, incomplete_tasks=incomplete_tasks)
        new_tasks = response.split("\n")
        return [{"task_name": task_name} for task_name in new_tasks if task_name.strip()]


class TaskPrioritizationChain(LLMChain):

    @classmethod
    def from_llm(cls, llm: BaseLLM, objective: str, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        task_prioritization_template = (
            "You are an task prioritization AI tasked with cleaning the formatting of and reprioritizing"
            " the following tasks: {task_names}."
            " Consider the ultimate objective of your team: {objective}."
            " Do not remove any tasks. Return the result as a numbered list, like:"
            " #. First task"
            " #. Second task"
            " Start the task list with number {next_task_id}."
        )
        prompt = PromptTemplate(
            template=task_prioritization_template,
            # partial_variables={"objective": objective},
            input_variables=["objective", "task_names", "next_task_id"],
        )
        return cls(llm=llm, prompt=prompt, verbose=verbose)

    def prioritize_tasks(self, this_task_id: int, task_list: List[Dict]) -> List[Dict]:
        task_names = [t["task_name"] for t in task_list]
        next_task_id = int(this_task_id) + 1
        response = self.run(task_names=task_names, next_task_id=next_task_id)
        new_tasks = response.split("\n")
        prioritized_task_list = []
        for task_string in new_tasks:
            if not task_string.strip():
                continue
            task_parts = task_string.strip().split(".", 1)
            if len(task_parts) == 2:
                task_id = task_parts[0].strip()
                task_name = task_parts[1].strip()
                prioritized_task_list.append({"task_id": task_id, "task_name": task_name})
        return prioritized_task_list


class TaskExecutionChain(LLMChain):
    vectorstore: VectorStore = Field(init=False)
    @classmethod
    def from_llm(cls, llm: BaseLLM, vectorstore: VectorStore, verbose: bool = True) -> LLMChain:
        """Get the response parser."""
        execution_template = (
            "You are an AI who performs one task based on the following objective: {objective}."
            " Take into account these previously completed tasks: {context}."
            " Your task: {task}."
            " Response:"
        )
        prompt = PromptTemplate(
            template=execution_template,
            input_variables=["objective", "context", "task"],
        )
        return cls(llm=llm, prompt=prompt, verbose=verbose, vectorstore=vectorstore)

    def _get_top_tasks(self, query: str, k: int) -> List[str]:
        """Get the top k tasks based on the query."""
        results = self.vectorstore.similarity_search_with_score(query, k=k)
        print(f"results: {results}")
        print(len(results))
        if not results:
            return []
        sorted_results, _ = zip(*sorted(results, key=lambda x: x[1], reverse=True))
        print(f"sorted_results: {sorted_results}")
        print(sorted_results[0])
        for item in sorted_results:
            print(item.metadata)
        return [str(item.metadata['task']) for item in sorted_results]

    def execute_task(self, objective: str, task: str, k: int =  5) -> str:
        context = self._get_top_tasks(query=objective, k=k)
        return self.run(objective=objective, context=context, task=task)

class BabySynth(BaseModel):
    objective: str = Field(alias="objective")
    task_list: deque = Field(default_factory=deque)
    task_creation_chain: TaskCreationChain = Field(...)
    task_prioritization_chain: TaskPrioritizationChain = Field(...)
    execution_chain: TaskExecutionChain = Field(...)
    task_id_counter: int = Field(1)

    def add_task(self, task: Dict):
        self.task_list.append(task)

    def print_task_list(self):
        print("\033[95m\033[1m" + "\n*****TASK LIST*****\n" + "\033[0m\033[0m")
        for t in self.task_list: 
            print(str(t["task_id"]) + ": " + t["task_name"])

    def print_next_task(self, task: Dict):
        print("\033[92m\033[1m" + "\n*****NEXT TASK*****\n" + "\033[0m\033[0m")
        print(str(task["task_id"]) + ": " + task["task_name"])

    def print_task_result(self, result: str):
        print("\033[93m\033[1m" + "\n*****TASK RESULT*****\n" + "\033[0m\033[0m")
        print(result)

    def run(self, max_iterations: Optional[int] = None):
        num_iters = 0
        while True:
            if self.task_list:
                self.print_task_list()

                task = self.task_list.popleft()
                self.print_next_task(task)
                
                result = self.execution_chain.execute_task(
                    self.objective, task["task_name"]
                )
                this_task_id = int(task["task_id"])
                self.print_task_result(result)

                result_id = f"result_{task['task_id']}"
                self.execution_chain.vectorstore.add_texts(
                    texts = [result],
                    metadata = [{"task": task["task_name"]}],
                    ids = [result_id]
                )

                new_tasks = self.task_creation_chain.get_next_task(
                    result, task["task_name"], [t["task_name"] for t in self.task_list]
                )
                for new_task in new_tasks:
                    self.task_id_counter += 1
                    new_task.update({"task_id": self.task_id_counter})
                    self.add_task(new_task)
                self.task_list = deque(
                    self.task_prioritization_chain.prioritize_tasks(
                        this_task_id,
                        list(self.task_list)
                    )
                )

                num_iters += 1
                if max_iterations is not None and num_iters == max_iterations:
                    print("\033[91m\033[1m" + "\n*****TASK ENDING*****\n" + "\033[0m\033[0m")
                    break


    @classmethod
    def from_llm_and_objective(
        cls,
        llm: BaseLLM,
        vectorstore: VectorStore,
        objective: str,
        initial_task: str,
        verbose: bool = False,
    ) -> "BabySynth":
        task_creation_chain = TaskCreationChain.from_llm(
            llm,
            objective,
            verbose=verbose
        )
        task_prioritization_chain = TaskPrioritizationChain.from_llm(
            llm,
            vectorstore,
            verbose=verbose
        )
        execution_chain = TaskExecutionChain.from_llm(
            llm,
            vectorstore,
            verbose=verbose
        )
        controller = cls(
            objective=objective,
            task_creation_chain=task_creation_chain,
            task_prioritization_chain=task_prioritization_chain,
            execution_chain=execution_chain
        )
        controller.add_task({"task_id": 1, "task_name": initial_task})
        return controller

verbose = True
max_iterations: Optional[int] = 3

baby_synth = BabySynth.from_llm_and_objective(
    llm = llm, 
    vectorstore = vectorstore,
    objective = OBJECTIVE,
    initial_task = INITIAL_TASK,
    verbose = verbose,
)

baby_synth.run(max_iterations=max_iterations)
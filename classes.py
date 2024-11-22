from typing import Dict, List


class Person:
    def __init__(self, first_name: str, last_name: str, id: int, tasks: List[Dict[str, str]]):
        self.first_name = first_name
        self.last_name = last_name
        self.id = id
        self.tasks = tasks
class Task:
    def __init__(self, id: int, task_name: str):
        self.id = id
        self.task_name = task_name
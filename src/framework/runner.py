from contextvars import ContextVar
from framework.planner import planner
from framework.task import Task


class Runner:
    def __init__(self):
        self.__tasks: list[Task] = []

    def add_task(self, task: Task):
        self.__tasks.append(task)

    def run(self):
        for task in planner(self.__tasks):
            task.func()

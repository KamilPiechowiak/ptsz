from p3.src.data_api import Instance
from p3.src.data_api import Task
from p3.src.generator_api import Generator
import random
import functools


class Generator136823(Generator):

    def generate(self, no_tasks: int, no_machines: int) -> Instance:
        tasks = []
        for _ in range(no_tasks):
            task_weight = random.randint(1, 10)
            task_duration = []
            for _ in range(no_machines):
                task_duration.append(random.randint(0, 50))
            task_due_date = random.randint(functools.reduce(lambda a, b: a + b, task_duration), no_tasks * 75)
            tasks.append(Task(task_duration, task_due_date, task_weight))
        return Instance(no_tasks, no_machines, tasks)

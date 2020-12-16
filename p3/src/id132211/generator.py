import functools
import math

from p3.src.data_api import Instance, Task
from p3.src.generator_api import Generator
import random


class Generator132211(Generator):

    def generate(self, no_tasks: int, no_machines: int) -> Instance:
        tasks = []
        for _ in range(no_tasks):
            durations = []
            for _ in range(no_machines):
                durations.append(random.randint(1, 10))
            due_date = random.randint(sum(durations), math.ceil((no_machines+no_machines*10)/2*no_tasks/5))
            weight = random.randint(4, 14)
            t = Task(durations, due_date, weight)
            tasks.append(t)
            tasks = sorted(tasks, key=lambda x: x.due_date)
        return Instance(no_tasks, no_machines, tasks)

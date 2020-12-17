from p3.src.data_api import Instance, Task
from p3.src.generator_api import Generator
from random import randint

class Generator136836(Generator):

    def generate(self, no_tasks: int, no_machines: int) -> Instance:
        tasks = []
        for _ in range(no_tasks):
            p = []
            for _ in range(no_machines):
                p.append(randint(1, 20))
            d = randint(2*sum(p), 60*no_tasks)
            w = randint(1, 10)
            tasks.append(Task(p, d, w))
        return Instance(no_tasks, no_machines, tasks)
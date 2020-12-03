from p2.src.data_api import Instance, Task
from p2.src.generator_api import Generator
from random import randint

class Generator136836(Generator):

    def generate(self, no_tasks: int, no_machines: int) -> Instance:
        machine_speeds = [1]
        for _ in range(no_machines-1):
            machine_speeds.append(randint(10, 30)/10)

        minR, maxR = 0, no_tasks*2
        minP, maxP = 1, 20

        tasks = []
        for _ in range(no_tasks):
            r = randint(minR, maxR)
            p = randint(minP, maxP)
            tasks.append(Task(p, r))

        instance = Instance(no_tasks, no_machines, machine_speeds, tasks)
        return instance


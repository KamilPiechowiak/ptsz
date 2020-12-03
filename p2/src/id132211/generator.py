from p2.src.data_api import Instance, Task
from p2.src.generator_api import Generator
import random


class Generator132211(Generator):

    def generate(self, no_tasks: int, no_machines: int) -> Instance:
        machine_speeds = [1.0]
        for i in range(no_machines-1):
            machine_speeds.append(random.randint(10, 50)/10)
        tasks = []
        for i in range(no_tasks):
            duration = random.randint(1, 9)
            avg_duration = (1+9)/2
            naive_speed = sum([1/x for x in machine_speeds])
            naive_end = int((avg_duration/naive_speed)*no_tasks)
            ready = random.randint(0, naive_end)
            tasks.append(Task(duration, ready))
        return Instance(no_tasks, no_machines, machine_speeds, tasks)

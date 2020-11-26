from p2.src.data_api import Instance
from typing import List

class Task:
    def __init__(self, p, r):
        self.p, self.r = p, r

def compute_loss(order, tasks, b):
    loss = 0
    for order_i, b_i in zip(order, b):
        t = 0
        for idx in order_i:
            task = tasks[idx]
            t = max(t, task.r)+task.p*b_i
            loss+=t-task.r
    return loss/len(tasks)

def read_instance(instance: Instance) -> (List[int], List[Task]):
    return instance.machine_speeds, [Task(task.duration, task.ready) for task in instance.tasks]
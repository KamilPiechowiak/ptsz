from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule

import random
def priority(a, b, w, d):
    return a * w - b * d

def score(tasks_list: list) -> int:
    D, w = 0, 0
    n = len(tasks_list)
    m = 3

    machine_time = m * [0]
    for task in tasks_list:
        duration = task[1].duration
        due_date = task[1].due_date
        weight = task[1].weight

        task_time = 0
        for num in range(m):
            task_time = max(machine_time[num], task_time)
            task_time += duration[num]
            machine_time[num] = task_time

        D += weight * max(0, task_time - due_date)
        w += weight
    w = max(w, 0.1)
    D /= w
    return D

class Algorithm136836(Algorithm):
    def run(self, in_data: Instance) -> Solution:
        n = in_data.no_tasks
        m = in_data.no_machines

        schedule = []
        end_tasks = []
        machine_time = m * [0]
        tasks = [i for i in zip(range(1, n+1), in_data.tasks)]
        result = []

        best = tasks
        for a in range(1, 14, 2):
            for b in range(5):
                tmp = sorted(tasks, key=lambda task: - priority(a, b, task[1].weight, task[1].due_date))
                if score(tmp) < score(best):
                    best = tmp

        schedule = best
        D = score(schedule)
        schedule = [task[0] for task in schedule]


        return Solution(score=D, schedule=Schedule(no_tasks=n, schedule=schedule))

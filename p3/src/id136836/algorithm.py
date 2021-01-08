from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule

import random


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


        best = tasks.copy()
        for _ in range(100):
            shuffle = best.copy()
            random.shuffle(shuffle)
            if score(shuffle) < score(best):
                best = shuffle

        for _ in range(100):
            swap = best.copy()
            i, j = random.randint(0, n-1), random.randint(0, n-1)
            best[i], best[j] = best[j], best[i]
            if score(swap) < score(best):
                best = swap


        schedule = best
        D = score(schedule)
        schedule = [task[0] for task in schedule]


        return Solution(score=D, schedule=Schedule(no_tasks=n, schedule=schedule))

from math import exp, log

from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule


def simple_wedd_sort(in_data: Instance):
    schedule = [i + 1 for i in range(in_data.no_tasks)]

    def factor(task):
        return exp(0.6 * log(task.due_date+1) + 0.4 * log(sum(task.duration))) / task.weight

    result = sorted(schedule, key=lambda x: factor(in_data.tasks[x-1]))
    return result


def objective(in_data: Instance, schedule: Schedule):
    m = in_data.no_machines
    c = [0] * m
    tasks = [in_data.tasks[i - 1] for i in schedule]
    cost = 0
    for t_i, task in enumerate(tasks):
        for m_j, duration in enumerate(task.duration):
            if m_j == 0:
                c[m_j] += duration
            else:
                c[m_j] = max(c[m_j - 1], c[m_j]) + duration
        cost += max(0, c[-1] - task.due_date) * task.weight
    cost = cost / sum([t.weight for t in tasks])
    return cost


class Algorithm136573(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        n = in_data.no_tasks
        schedule = Schedule(n, simple_wedd_sort(in_data))
        obj = objective(in_data, schedule)
        return Solution(obj, schedule=schedule)
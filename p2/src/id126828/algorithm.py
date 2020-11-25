from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule
import numpy as np
from itertools import zip_longest


class Algorithm126828(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        def chunks(l, n):
            """ Yield n successive chunks from l.
            """
            newn = int(len(l) / n)
            for i in range(0, n - 1):
                yield l[i * newn:i * newn + newn]
            yield l[n * newn - newn:]

        sorted_tasks = sorted(enumerate(in_data.tasks, 1), key=lambda x: x[1].duration,reverse=True)
        machines = sorted(enumerate(in_data.machine_speeds), key=lambda x: x[1])
        # split tasks into equal parts to machines
        to_machines = chunks(sorted_tasks, in_data.no_machines)
        schedule = [[]] * in_data.no_machines
        local_solutions = [0.0] * in_data.no_machines
        for machine_num, machine_speed in machines:
            for tasks in to_machines:
                # for every task use timer to count solution and add
                # add this tasks  to this machine
                local_timer = 0

                for ind, task in tasks:
                    schedule[machine_num].append(ind)
                    local_timer = max(local_timer, task.ready)
                    local_timer += task.duration * machine_speed
                    local_solutions[machine_num] += local_timer - task.ready
                    # add to current machine task with id.

        global_solution = sum(local_solutions) / in_data.no_tasks
        return Solution(score=global_solution,
                        schedule=Schedule(n=in_data.no_tasks, m=in_data.no_machines, schedule=schedule))

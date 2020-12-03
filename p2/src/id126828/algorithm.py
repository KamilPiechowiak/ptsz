from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule
import numpy as np
from itertools import zip_longest


class Algorithm126828(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        def find_best(task_checked):
            solutions = {}
            timer = [0] * in_data.no_machines
            for machine_num, machine in machines:
                timer[machine_num] = max(local_timers[machine_num], task_checked.ready)
                timer[machine_num] += task_checked.duration * machine
                solutions[machine_num] = timer[machine_num] - task.ready
            #choose best machine
            chosen_machine = min(solutions, key=solutions.get)
            #increment timer and solution on local chosen machine
            local_solutions[chosen_machine] += solutions[chosen_machine]
            local_timers[chosen_machine] = timer[chosen_machine]

            return chosen_machine

        sorted_tasks = sorted(enumerate(in_data.tasks, 1), key=lambda x: (x[1].ready,x[1].duration))
        machines = list(enumerate(in_data.machine_speeds))
        # split tasks into equal parts to machines
        local_solutions = [0.0] * in_data.no_machines
        local_timers = [0.0] * in_data.no_machines
        local_schedules = []
        [local_schedules.append([]) for i in range(5)]
        #for every task find where is minimum value and add this to schedule.
        for ind, task in sorted_tasks:
            #find best machine for this solution
            append_task_to = find_best(task)
            #append this tasks to chosen machine
            local_schedules[append_task_to].append(ind)


        global_solution = sum(local_solutions) / in_data.no_tasks
        return Solution(score=global_solution,
                        schedule=Schedule(n=in_data.no_tasks, m=in_data.no_machines, schedule=local_schedules))

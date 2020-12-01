from p2.src.algorithm_api import *
from p2.src.data_api import Schedule
import pandas as pd


class Algorithm136811(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        schedule = [[] for _ in range(in_data.no_machines)]

        tasks = pd.DataFrame(data=[[t.ready, t.duration] for t in in_data.tasks])
        # print(tasks)
        # in_data.tasks.sort(key=lambda x: x.ready)
        tasks = tasks.sort_values(by=[0, 1], ascending=[True, False])
        # print(tasks)
        act_machine = 0
        for i, task in tasks.iterrows():
            schedule[act_machine].append(int(task.name) + 1)
            act_machine += 1
            act_machine %= in_data.no_machines
        # print(schedule)

        current_moment = in_data.no_machines * [0]
        current_score = in_data.no_machines * [0]

        for num, machine in enumerate(schedule):
            for task_no in machine:
                task = in_data.tasks[task_no - 1]
                current_moment[num] = max(current_moment[num], task.ready)
                current_moment[num] += task.duration * in_data.machine_speeds[num]
                current_score[num] += current_moment[num] - task.ready

        result = sum(current_score) / in_data.no_tasks
        return Solution(result, Schedule(in_data.no_tasks, in_data.no_machines, schedule))

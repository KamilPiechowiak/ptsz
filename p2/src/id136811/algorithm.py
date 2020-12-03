from typing import List
from p2.src.algorithm_api import *
from p2.src.data_api import Schedule
import pandas as pd


class Algorithm136811(Algorithm):

    @staticmethod
    def calc_score(in_data: Instance, schedule: List) -> float:
        current_moment = in_data.no_machines * [0]
        current_score = in_data.no_machines * [0]

        for num, machine in enumerate(schedule):
            for task_no in machine:
                task = in_data.tasks[task_no - 1]
                current_moment[num] = max(current_moment[num], task.ready)
                current_moment[num] += task.duration * in_data.machine_speeds[num]
                current_score[num] += current_moment[num] - task.ready

        return sum(current_score) / in_data.no_tasks

    @staticmethod
    def alg1(in_data: Instance) -> Solution:
        schedule = [[] for _ in range(in_data.no_machines)]

        tasks = pd.DataFrame(data=[[t.ready, t.duration] for t in in_data.tasks])
        # print(tasks)
        # in_data.tasks.sort(key=lambda x: x.ready)
        tasks = tasks.sort_values(by=[0, 1], ascending=[True, False])
        # tasks = tasks.sort_values(by=[1, 0], ascending=[True, False])

        # print(tasks)
        machines = dict()
        for inx, m in enumerate(in_data.machine_speeds):
            machines[inx] = m

        srt_mach = sorted(machines.items(), key=lambda it: it[1])
        # print(srt_mach)

        act_machine = 0
        for i, task in tasks.iterrows():
            schedule[srt_mach[act_machine][0]].append(int(task.name) + 1)
            act_machine += 1
            act_machine %= in_data.no_machines
        # print(schedule)

        result = Algorithm136811.calc_score(in_data, schedule)
        return Solution(result, Schedule(in_data.no_tasks, in_data.no_machines, schedule))

    @staticmethod
    def alg2(in_data: Instance) -> Solution:
        schedule = [[] for _ in range(in_data.no_machines)]

        tasks = pd.DataFrame(data=[[t.ready, t.duration] for t in in_data.tasks])
        tasks = tasks.sort_values(by=[0, 1], ascending=[True, False])
        # tasks = tasks.sort_values(by=[0], ascending=[True])

        machines = dict()
        for inx, m in enumerate(in_data.machine_speeds):
            machines[inx] = [m, 0]

        srt_mach = sorted(machines.items(), key=lambda it: it[1][0])
        # print(srt_mach)

        # sum_p = sum([t.duration for t in in_data.tasks])
        # sum_mach_pow = sum([1.0 / b for b in in_data.machine_speeds])
        # opt_end = sum_p / sum_mach_pow

        for i, task in tasks.iterrows():
            added = False
            for machine in range(5):
                if srt_mach[machine][1][1] <= task[0]:
                    schedule[srt_mach[machine][0]].append(int(task.name) + 1)
                    srt_mach[machine][1][1] = max(task[0], srt_mach[machine][1][1]) + \
                                              task[1] * in_data.machine_speeds[srt_mach[machine][0]]
                    added = True
                    break
            if not added:
                tmp = []
                for m in range(5):
                    tmp.append((m, max(srt_mach[m][1][1], task[0]) + task[1]* in_data.machine_speeds[srt_mach[m][0]]))
                best = min(tmp, key=lambda it: it[1])
                schedule[srt_mach[best[0]][0]].append(int(task.name) + 1)
                srt_mach[best[0]][1][1] = best[1]

        result = Algorithm136811.calc_score(in_data, schedule)
        return Solution(result, Schedule(in_data.no_tasks, in_data.no_machines, schedule))

    def run(self, in_data: Instance) -> Solution:
        return self.alg2(in_data)

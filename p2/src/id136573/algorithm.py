from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule, Task


class ScheduledTask:
    def __init__(self, id, r, p, end):
        self.id = id
        self.r = r
        self.p = p
        self.end = end


class Algorithm136573(Algorithm):


    def run(self, in_data: Instance) -> Solution:
        n = in_data.no_tasks
        m = in_data.no_machines
        tasks = [ScheduledTask(i+1, t.ready, t.duration, 0) for i, t in enumerate(in_data.tasks)]
        tasks.sort(key=lambda t: t.p)

        c_m_i = [0] * m
        ans = [[] for _ in range(m)]
        for i, task in enumerate(tasks):
            min_m = 0
            min_cost = 1e7
            tmp_last_competed = [0.0] * m
            for m_i, machine, speed in zip(range(m), ans, in_data.machine_speeds):
                if len(machine) == 0:
                    cost = task.p * speed
                    if cost < min_cost:
                        min_m = m_i
                        min_cost = cost
                        tmp_last_competed[m_i] = task.r + cost
                        continue
                tmp_last_competed[m_i] = max(c_m_i[m_i], task.r) + task.p * speed
                cost = tmp_last_competed[m_i] - task.r
                if cost < min_cost:
                    min_m = m_i
                    min_cost = cost
            ans[min_m].append(task.id)
            task.end = max(c_m_i[min_m], task.r) + task.p * in_data.machine_speeds[min_m]
            c_m_i[min_m] = task.end


        obj = 0
        for num, machine in enumerate(ans):
            c = 0
            for idx in machine:
                task = in_data.tasks[idx - 1]
                c = max(c, task.ready) + (task.duration * in_data.machine_speeds[num])
                obj += c - task.ready
        obj = obj / n

        return Solution(obj, Schedule(n, m, ans))

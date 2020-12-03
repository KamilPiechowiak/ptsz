from typing import NamedTuple
from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule

from p2.src.id132211.evaluator import Evaluator132211


class IndexedTask(NamedTuple):
    duration: int
    ready: int
    index: int


class Algorithm132211(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        n = in_data.no_tasks
        m = in_data.no_machines
        machine_speeds = sorted(in_data.machine_speeds)
        r = range(m)
        r = sorted(r, key=in_data.machine_speeds.__getitem__)
        schedule = [[] for _ in range(m)]
        ready_tasks = []
        done = [0 for _ in range(m)]
        tasks_by_readiness = [IndexedTask(task.duration, task.ready, index) for index, task in enumerate(in_data.tasks, 1)]
        tasks_by_readiness = sorted(tasks_by_readiness, key=lambda x: x.ready)
        mean_speed = sum(machine_speeds)/m
        time = tasks_by_readiness[0].ready
        while len(tasks_by_readiness) > 0 or len(ready_tasks) != 0:
            while len(tasks_by_readiness) > 0 and tasks_by_readiness[0].ready <= time:
                ready_tasks.append(tasks_by_readiness.pop(0))

            task_finish = min(done)
            machine = 0
            for t in done:
                if t == task_finish:
                    break
                machine += 1
            if len(ready_tasks) == 0:
                continue
            best_index = 0
            reverse = -1 if machine_speeds[machine] < mean_speed else 1
            best_task_duration = 1e18
            for index, task in enumerate(ready_tasks):
                if reverse * task.duration < best_task_duration:
                    best_task_duration = reverse * task.duration
                    best_index = index
            schedule[machine].append(ready_tasks.pop(best_index).index)
            done[machine] = time + reverse * best_task_duration * machine_speeds[machine]
            time = max(min(done), -1 if len(tasks_by_readiness) == 0 else tasks_by_readiness[0].ready)

        for i, c in zip(r, list(schedule)):
            schedule[i] = c
        schedule = Schedule(n, m, schedule)
        solution = Solution(0, schedule)
        return Solution(Evaluator132211().evaluate(in_data, solution).value, schedule)

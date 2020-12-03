from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution, Schedule


class Algorithm136836(Algorithm):
    def run(self, in_data: Instance) -> Solution:
        score = 0
        n = in_data.no_tasks
        m = in_data.no_machines

        schedule =[[] for i in range(m)]
        machines = [i for i in zip(range(m), m*[0], in_data.machine_speeds)]
        tasks = [i for i in zip(range(1, n+1), in_data.tasks)]

        for task in sorted(tasks, key=lambda task: task[1].ready):
            task_id = task[0]
            ready = task[1].ready
            duration = task[1].duration

            machine = min(machines, key=lambda machine: machine[1] + duration * machine[2])
            machine_id = machine[0]
            time = machine[1]
            speed = machine[2]

            schedule[machine_id].append(task_id)
            C = max(ready+duration*speed, time+duration*speed)
            machines[machine_id] = (machine_id, C, speed)

            score += C - ready
        score /= n
        return Solution(score=score, schedule=Schedule(n, m, schedule))

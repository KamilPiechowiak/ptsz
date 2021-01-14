from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule
from p3.src.id127183.evaluator import Evaluator127183


class Job:

    def __init__(self, id, duration, due_date, weight):
        self.id = id
        self.duration = duration
        self.due_date = due_date
        self.weight = weight


class Algorithm127183(Algorithm):

    def H2I(self, jobs):
        J1, J2 = [], []
        for job in jobs:
            p1, p2, p3 = job.duration
            if p1 <= p2 + p3:
                J1.append(job)
            else:
                J2.append(job)
        J1.sort(key=lambda x: (x.duration[0] * float(x.due_date/x.weight)))
        J2.sort(key=lambda x: (x.duration[1] + x.duration[2]) * float(x.weight/(x.due_date+0.00000001)), reverse=True)
        return J1, J2

    def run(self, in_data: Instance) -> Solution:
        jobs = [Job(counter+1, task.duration, task.due_date, task.weight) for counter, task in enumerate(in_data.tasks)]
        jobs.sort(key=lambda x: (sum(x.duration) * float(x.due_date/x.weight)))
        schedule = Schedule(in_data.no_tasks, [job.id for job in jobs])
        score = Evaluator127183().evaluate(in_data, Solution(0.0, schedule)).value
        return Solution(score, schedule)

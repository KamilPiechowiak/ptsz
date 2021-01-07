import numpy as np

from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule
from p3.src.id136775.evaluator import Evaluator136775


class Algorithm136775(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        tasks = map(lambda x: (x[0] + 1, x[1]), enumerate(in_data.tasks))
        ids = list(map(lambda x: x[0], sorted(tasks, key=lambda tup: tup[1].due_date)))

        schedule = Schedule(in_data.no_tasks, ids)
        score = Evaluator136775().score(in_data, schedule)
        return Solution(score, schedule)

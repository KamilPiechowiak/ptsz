from p3.src.algorithm_api import Algorithm
from p3.src.data_api import Instance, Solution, Schedule
from src.id136810.alg.scheduler import Scheduler
from src.id136810.evaluator import getScore


class Algorithm136810(Algorithm):
    def run(self, in_data: Instance) -> Solution:
        scheduler = Scheduler(in_data.tasks)
        scheduler.init_sort()
        scheduled_jobs = scheduler.schedule2()
        schedule = list(map(lambda x: x.number + 1, scheduled_jobs))
        score = getScore(in_data, schedule)
        #exit()
        return Solution(score, Schedule(in_data.no_tasks, schedule))


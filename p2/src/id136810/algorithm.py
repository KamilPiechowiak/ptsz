from p2.src.id136810.alg.Utils import getSolution
from p2.src.id136810.alg.Scheduler import Scheduler
from p2.src.algorithm_api import Algorithm
from p2.src.data_api import Instance, Solution


class Algorithm136810(Algorithm):

    def run(self, in_data: Instance) -> Solution:
        scheduler = Scheduler(in_data)
        scheduler.sortByReadyMoment()
        for task in scheduler.tasks:
            scheduler.scheduleJob(task)
        return getSolution(in_data, scheduler.getFinalSchedule())

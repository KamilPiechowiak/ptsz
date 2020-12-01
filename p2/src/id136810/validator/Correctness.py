import numpy as np
from p2.src.data_api import Solution, Schedule

class Correctness:
    def __init__(self):
        self.weight = 0

    def flatten(self, machines):
        return [task_no for machine_list in machines for task_no in machine_list]

    def checkLength(self, size, schedule: Schedule):
        assert size == len(self.flatten(schedule))

    def checkDoubles(self, size, schedule: Schedule):
            unique = np.unique(self.flatten(schedule))
            assert len(unique) == size

    def checkCorrectness(self, size, instance: Solution):
        self.checkLength(size, instance.schedule)
        self.checkDoubles(size, instance.schedule)

    def checkCriterium(self, calculatedCriterium, outputCriterium):
        return calculatedCriterium == outputCriterium
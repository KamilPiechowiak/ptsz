import numpy as np
from p2.src.data_api import Solution, Schedule
from p2.properties import EPS


class Correctness:
    def __init__(self):
        self.weight = 0

    def flatten(self, machines):
        return [task_no for machine_list in machines for task_no in machine_list]

    def checkCriterium(self, calculatedCriterium, outputCriterium):
        return abs(calculatedCriterium - outputCriterium) < EPS

from abc import ABC, abstractmethod, ABCMeta
from typing import NamedTuple, List, NamedTupleMeta

import numpy as np

from p2.src.utils import lmap


class Dumpable(ABC):

    @staticmethod
    @abstractmethod
    def load(path: str):
        pass

    @abstractmethod
    def dump(self, path: str):
        pass


class Task(NamedTuple):
    duration: int
    ready: int


class ABCNamedTupleMeta(ABCMeta, NamedTupleMeta):
    pass


class Instance(NamedTuple, Dumpable, metaclass=ABCNamedTupleMeta):
    no_tasks: int
    no_machines: int
    machine_speeds: List[int]
    tasks: List[Task]

    @staticmethod
    def load(path: str) -> 'Instance':
        with open(path) as file:
            n = int(file.readline())
            b_array = lmap(int, file.readline().split(' ')[:5])
            tasks = lmap(lambda t: Task(*t), [list(map(int, file.readline().split(' ')[:2])) for i in range(n)])
            data_in = Instance(no_tasks=n,
                               no_machines=len(b_array),
                               machine_speeds=b_array,
                               tasks=tasks)
            return data_in

    def dump(self, path: str):
        with open(path, 'w') as file:
            file.write(f'{self.no_tasks}\n')
            file.write(f'{" ".join(map(str, self.machine_speeds))}\n')
            for task in self.tasks:
                file.write(f'{task.duration} {task.ready}\n')


class Schedule(list):
    """Creates tasks' scheduling
        :param n: number of tasks
        :param m: number of machines
        :param schedule: list of m lists with tasks assigned to each machine (total number of tasks should be equal to n)
    """

    def __init__(self, n: int, m: int, schedule: list):
        self.n, self.m = n, m
        if not self.is_correct(n, m, schedule):
            raise ValueError('This is not a 1 to N permutation')
        super(Schedule, self).__init__(schedule)

    @staticmethod
    def is_correct(n: int, m: int, schedule: List[List[int]]) -> bool:
        flags = np.zeros(n, dtype=bool)
        for machine_tasks in schedule:
            for idx in machine_tasks:
                if idx < 1 or idx > n:
                    return False
                flags[idx - 1] = True
        return all(flags)

    @staticmethod
    def get_dummy_schedule(n: int, m: int) -> 'Schedule':
        tasks_num = [n // m] * m
        tasks_num[m - 1] = n - (n // m) * (m - 1)
        schedule = []
        start = 1
        for i in range(m):
            schedule.append([j for j in range(start, start + tasks_num[i])])
            start += tasks_num[i]

        return Schedule(n, m, schedule)


def check_if_int(value):
    try:
        int(value)
        return True
    except:
        return False


class Solution(NamedTuple, Dumpable, metaclass=ABCNamedTupleMeta):
    score: float
    schedule: Schedule

    @staticmethod
    def load(path: str):
        with open(path) as file:
            score = float(file.readline())
            schedule = [
                [int(idx) for idx in line.split(' ') if check_if_int(idx)]
                for line in file.readlines()]
            m = len(schedule)
            n = sum([len(schedule_i) for schedule_i in schedule])
            return Solution(score=score, schedule=Schedule(n=n, m=m, schedule=schedule))

    def dump(self, path: str):
        with open(path, 'w') as file:
            file.write(f'{self.score}\n')
            file.write("\n".join([" ".join(lmap(str, schedule_i)) for schedule_i in self.schedule]))

    @staticmethod
    def get_dummy_solution(n: int, m: int):
        return Solution(score=0, schedule=Schedule.get_dummy_schedule(n, m))

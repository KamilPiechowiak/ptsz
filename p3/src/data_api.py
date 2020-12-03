from abc import ABC, abstractmethod, ABCMeta
from typing import NamedTuple, List, NamedTupleMeta

import numpy as np

from p3.src.utils import lmap


class Dumpable(ABC):

    @staticmethod
    @abstractmethod
    def load(path: str):
        pass

    @abstractmethod
    def dump(self, path: str):
        pass


class Task(NamedTuple):
    duration: List[int]
    due_date: int
    weight: int


class ABCNamedTupleMeta(ABCMeta, NamedTupleMeta):
    pass


class Instance(NamedTuple, Dumpable, metaclass=ABCNamedTupleMeta):
    no_tasks: int
    no_machines: int
    tasks: List[Task]

    @staticmethod
    def load(path: str) -> 'Instance':
        with open(path) as file:
            n = int(file.readline())
            tasks = lmap(lambda t: Task(t[0:3], t[3], t[4]), [list(map(int, file.readline().split(' ')[:5])) for i in range(n)])
            data_in = Instance(no_tasks=n,
                               no_machines=3,
                               tasks=tasks)
            return data_in

    def dump(self, path: str):
        with open(path, 'w') as file:
            file.write(f'{self.no_tasks}\n')
            for task in self.tasks:
                file.write(f'{" ".join(map(str,task.duration))} {task.due_date} {task.weight}\n')


class Schedule(list):
    """Creates tasks' scheduling
        :param n: number of tasks
        :param schedule: list of tasks's ids
    """

    def __init__(self, no_tasks: int, schedule: List[int]):
        self.no_tasks = no_tasks
        if not self.is_correct(no_tasks, schedule):
            raise ValueError('This is not a 1 to N permutation')
        super(Schedule, self).__init__(schedule)

    @staticmethod
    def is_correct(no_tasks: int, schedule: List[int]) -> bool:
        flags = np.zeros(no_tasks, dtype=bool)
        for idx in schedule:
            if idx < 1 or idx > no_tasks:
                return False
            flags[idx - 1] = True
        return all(flags)

    @staticmethod
    def get_dummy_schedule(no_tasks: int) -> 'Schedule':
        schedule = [i+1 for i in range(no_tasks)]
        return Schedule(no_tasks, schedule)


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
            schedule = [int(idx) for idx in file.readline().split(' ') if check_if_int(idx)]
            return Solution(score=score, schedule=Schedule(n=len(schedule), schedule=schedule))

    def dump(self, path: str):
        with open(path, 'w') as file:
            file.write(f'{self.score}\n')
            file.write(" ".join(map(str, self.schedule)))

    @staticmethod
    def get_dummy_solution(n: int):
        return Solution(score=0, schedule=Schedule.get_dummy_schedule(n))

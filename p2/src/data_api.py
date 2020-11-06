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
    machine_speeds: List[float]
    tasks: List[Task]

    @staticmethod
    def load(path: str) -> 'Instance':
        with open(path) as file:
            n = int(file.readline())
            b_array = lmap(float, file.readline().split(' '))
            tasks = lmap(Task, [list(map(int, file.readline().split(' '))) for i in range(n)])
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


class Permutation(list):
    def __init__(self, vlist):
        if not self.is_correct(vlist):
            raise ValueError('This is not a 1 to N permutation')
        super(Permutation, self).__init__(vlist)

    @staticmethod
    def is_correct(permutation) -> bool:
        n = len(permutation)
        flags = np.zeros(n, dtype=bool)
        for i in range(0, n):
            flags[permutation[i] - 1] = True

        return all(flags)


class Solution(NamedTuple, Dumpable, metaclass=ABCNamedTupleMeta):
    score: int
    permutation: Permutation

    @staticmethod
    def load(path: str):
        with open(path) as file:
            score = int(file.readline())
            permutation = Permutation(lmap(int, file.readline().split(' ')))
            return Solution(score=score, permutation=permutation)

    def dump(self, path: str):
        with open(path, 'w') as file:
            file.write(f'{self.score}\n')
            file.write(f'{" ".join(self.permutation)}\n')

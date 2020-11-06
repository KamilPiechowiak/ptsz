import time
from abc import ABC, abstractmethod
from typing import NamedTuple

from p2.src.algorithm_api import Solution, Algorithm
from p2.src.data_api import Instance


class EvaluatorOutput(NamedTuple):
    correct: bool
    value: float
    time: float


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, in_data: Instance, output: Solution, time: float = 0) -> EvaluatorOutput:
        pass

    def validate_schedule(self, in_data: Instance, output: Solution) -> EvaluatorOutput:
        return self.evaluate(in_data, output)

    def validate_algorithm(self, in_data: Instance, algorithm: Algorithm) -> EvaluatorOutput:
        time_1 = time.time()
        output = algorithm.run(in_data)
        time_2 = time.time()
        output = self.evaluate(in_data, output, (time_2 - time_1) * 1000)
        return output

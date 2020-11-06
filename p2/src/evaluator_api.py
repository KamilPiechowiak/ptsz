from abc import ABC, abstractmethod
from typing import NamedTuple

from p2.src.algorithm_api import Solution, Algorithm
from p2.src.data_api import Instance


class EvaluatorOutput(NamedTuple):
    correct: bool
    value: int


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, in_data: Instance, output: Solution) -> EvaluatorOutput:
        pass

    def validate_permutation(self, in_data: Instance, output: Solution) -> EvaluatorOutput:
        return self.evaluate(in_data, output)

    def validate_algorithm(self, in_data: Instance, algorithm: Algorithm) -> EvaluatorOutput:
        output = algorithm.run(in_data)
        return self.evaluate(in_data, output)

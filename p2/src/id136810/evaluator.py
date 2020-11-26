from p2.src.data_api import Instance, Solution
from p2.src.evaluator_api import EvaluatorOutput, Evaluator

from p2.src.id136810.validator.Correctness import Correctness
from p2.src.id136810.validator.Criterium import Criterium


class Evaluator136810(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        correctness = Correctness()

        correctness.checkCorrectness(in_data.no_tasks, output)

        criterium = Criterium(in_data, output)

        criteriumValue = criterium.getCriterium()

        evaluatorOuput = EvaluatorOutput(
            correctness.checkCriterium(criteriumValue, output.score),
            criteriumValue,
            time
        )
        return evaluatorOuput

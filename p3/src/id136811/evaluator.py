from p3.src.data_api import Instance, Solution
from p3.src.evaluator_api import EvaluatorOutput, Evaluator
from p3.properties import EPS


class Evaluator136811(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = 0) -> EvaluatorOutput:
        score = 0
        d = 0
        curr = [0, 0, 0]
        for inx in output.schedule:
            t = in_data.tasks[inx - 1]
            for i, _ in enumerate(curr):
                if i != 0:
                    p = max(curr[i - 1], curr[i])
                    curr[i] = p + t.duration[i]
                else:
                    curr[i] += t.duration[i]
            score += max(0, max(curr) - t.due_date) * t.weight
            d += t.weight
        score /= d

        return EvaluatorOutput(abs(score - output.score) <= EPS, score, time)

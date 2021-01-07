from p3.properties import EPS
from p3.src.data_api import Instance, Solution
from p3.src.evaluator_api import Evaluator, EvaluatorOutput


class Evaluator126828(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = 0) -> EvaluatorOutput:
        score = 0.0
        moments = [0 for _ in range(in_data.no_machines)]
        for task_index in output.schedule:
            task = in_data.tasks[task_index - 1]
            moments[0] += task.duration[0]
            moments[1] = max(moments[0], moments[1]) + task.duration[1]
            moments[2] = max(moments[1], moments[2]) + task.duration[2]
            score += max(0, moments[2] - task.due_date) * task.weight
        score /= sum([task.weight for task in in_data.tasks])
        correct = abs(score - output.score) <= EPS
        if score != 0:
            correct = correct or abs(score - output.score) / score <= EPS

        return EvaluatorOutput(correct, score, time)

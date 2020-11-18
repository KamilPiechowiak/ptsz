from p2.src.data_api import Instance, Solution
from p2.src.evaluator_api import EvaluatorOutput, Evaluator


class Evaluator136836(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        current_moment = in_data.no_machines * [0]
        current_score = in_data.no_machines * [0]
        for num, machine in enumerate(output.schedule):
            for task_no in machine:
                task = in_data.tasks[task_no-1]
                current_moment[num] = max(current_moment[num], task.ready)
                current_moment[num] += task.duration
                current_score[num] += current_moment[num] - task.ready

        result = sum(current_score) / len(current_score)
        return EvaluatorOutput(output.score==result, result, 0)


from p2.src.data_api import Instance, Solution
from p2.src.evaluator_api import EvaluatorOutput, Evaluator
from p2.properties import EPS
import numpy as np
import time as t


class Evaluator126828(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        current_score = np.zeros(in_data.no_machines)
        for num, machine in enumerate(output.schedule):
            current_moment = 0
            for task_no in machine:
                task = in_data.tasks[task_no - 1]
                current_moment = max(current_moment, task.ready)
                current_moment += task.duration * in_data.machine_speeds[num]
                current_score[num] += current_moment - task.ready
        # (loss - my_loss) / my_loss < EPS or (loss - my_loss) < EPS
        result = sum(current_score) / in_data.no_tasks
        correct = False
        if (output.score - result) / result < EPS or (output.score - result) < EPS:
            correct = True
        return EvaluatorOutput(correct, result, time)

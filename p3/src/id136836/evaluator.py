from p3.src.data_api import Instance, Solution
from p3.src.evaluator_api import EvaluatorOutput, Evaluator


class Evaluator136836(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        machine_time = in_data.no_machines * [0]
        D = 0
        w = 0
        for task in in_data.tasks:
            task_time = 0
            for num in range(in_data.no_machines):
                task_time = max(machine_time[num], task_time)
                task_time += task.duration[num]
                machine_time[num] = task_time
            D += task.weight * max(0, task_time - task.due_date)
            w += task.weight
        D /= w
        return EvaluatorOutput(D == output.score, D, time)


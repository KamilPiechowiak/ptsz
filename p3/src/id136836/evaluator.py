from p3.src.data_api import Instance, Solution
from p3.src.evaluator_api import EvaluatorOutput, Evaluator
from p3.properties import EPS

class Evaluator136836(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        m = in_data.no_machines
        D, w = 0, 0
        machine_time = m * [0]

        for t in output.schedule:
            task = in_data.tasks[t - 1]
            task_time = 0
            duration = task.duration
            due_date = task.due_date
            weight = task.weight
            for num in range(m):
                task_time = max(machine_time[num], task_time)
                task_time += task.duration[num]
                machine_time[num] = task_time
            D += task.weight * max(0, task_time - due_date)
            w += task.weight
        D /= w
        correct = abs(D - output.score) <= EPS
        return EvaluatorOutput(correct, D, time)

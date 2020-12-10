from p3.src.data_api import Instance, Solution
from p3.src.evaluator_api import EvaluatorOutput, Evaluator
import functools


class Evaluator136823(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        total_latency = 0
        weights_sum = 0
        machine_times = [0 for _ in range(in_data.no_machines)]
        for task in in_data.tasks:
            weights_sum += task.weight
            task_time = 0
            for i in range(in_data.no_machines):
                task_time = max(task_time, machine_times[i]) + task.duration[i]
                machine_times[i] = task_time
            total_latency += max(task_time - task.due_date, 0) * task.weight
        average_latency = total_latency / weights_sum
        return EvaluatorOutput(average_latency == output.score, average_latency, time)

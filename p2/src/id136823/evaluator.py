from p2.src.data_api import Instance, Solution
from p2.src.evaluator_api import EvaluatorOutput, Evaluator


class Evaluator136823(Evaluator):

    def evaluate(self, in_data: Instance, output: Solution, time: float = None) -> EvaluatorOutput:
        result = self.get_score(output.score, output.schedule, in_data.no_tasks, in_data.tasks, in_data.machine_speeds)
        return EvaluatorOutput(result[0], result[1], time)

    @staticmethod
    def get_score(value, orders, number_tasks, tasks, speeds):
        score = 0
        for machine, order in enumerate(orders):
            current_time = 0
            for number_task in order:
                current_task = tasks[number_task - 1]
                if current_time > current_task.ready:
                    score += current_time - current_task.ready + current_task.duration * speeds[machine]
                    current_time += current_task.duration * speeds[machine]
                else:
                    score += current_task.duration * speeds[machine]
                    current_time = current_task.ready + current_task.duration * speeds[machine]
        average_score = score / number_tasks
        return average_score == value, average_score